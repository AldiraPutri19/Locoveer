from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the TFLite model
MODEL_PATH = 'collaborative_filtering_recommendation_system.tflite'
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

# Extract input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load data
travel_destinations_df = pd.read_csv('travel_destinations_cleaned.csv')
eco_impact_matrix_df = pd.read_csv('eco_impact_matrix.csv')

def calculate_eco_score(matrix):
    weights = {
        "Eco_Friendliness": -0.4,
        "Renewable_Energy_Usage": -0.4,
        "Waste_Management": 0.3,
        "Public_Transport_Access": 0.1,
        "Cultural_Preservation_Effort": 0.2,
    }

    # Ensure all columns are numeric
    for column in weights.keys():
        matrix[column] = pd.to_numeric(matrix[column], errors="coerce")

    matrix["Eco_Score"] = (
        (matrix["Eco_Friendliness"] * weights["Eco_Friendliness"]) +
        (matrix["Renewable_Energy_Usage"] * weights["Renewable_Energy_Usage"]) +
        (matrix["Waste_Management"] * weights["Waste_Management"]) +
        (matrix["Public_Transport_Access"] * weights["Public_Transport_Access"]) +
        (matrix["Cultural_Preservation_Effort"] * weights["Cultural_Preservation_Effort"])
    )

    # Handle NaN values and normalize scores
    matrix["Eco_Score"] = matrix["Eco_Score"].fillna(0)
    matrix["Eco_Score"] = (matrix["Eco_Score"] - matrix["Eco_Score"].min()) / (
        matrix["Eco_Score"].max() - matrix["Eco_Score"].min()
    )
    return matrix[["Destination_ID", "Eco_Score"]]

# Calculate eco scores and merge with destinations
eco_scores = calculate_eco_score(eco_impact_matrix_df)
travel_destinations_df = travel_destinations_df.merge(eco_scores, on="Destination_ID", how="left")

# Create user and destination mappings
user_mapping = {id_: idx for idx, id_ in enumerate(travel_destinations_df["Destination_ID"].unique())}
destination_mapping = {id_: idx for idx, id_ in enumerate(travel_destinations_df["Destination_ID"].unique())}

def generate_recommendations(
    interpreter, user_id, destination_ids, travel_destinations, category_filter=None,
    top_n=10, rating_weight=0.6, eco_weight=0.4
):
    test_rating = {}
    for dest_id in destination_ids:
        # Filter by category if specified
        if category_filter and travel_destinations.loc[
            travel_destinations["Destination_ID"] == dest_id, "Category"].iloc[0] != category_filter:
            continue

        # Prepare input tensors
        user_tensor = np.array([[user_id]], dtype=np.float32)
        dest_tensor = np.array([[dest_id]], dtype=np.float32)

        interpreter.set_tensor(input_details[0]['index'], user_tensor)
        interpreter.set_tensor(input_details[1]['index'], dest_tensor)

        # Run inference
        interpreter.invoke()

        # Extract predictions
        predicted_rating = interpreter.get_tensor(output_details[0]['index'])[0][0]

        eco_score = travel_destinations.loc[
            travel_destinations["Destination_ID"] == dest_id, "Eco_Score"].fillna(0).iloc[0]

        combined_score = (predicted_rating * rating_weight) + (eco_score * eco_weight)
        test_rating[dest_id] = {
            "predicted_rating": predicted_rating,
            "eco_score": eco_score,
            "combined_score": combined_score,
        }

    # Get top destinations
    top_destinations = sorted(test_rating, key=lambda x: test_rating[x]["combined_score"], reverse=True)[:top_n]

    recommendations = []
    for dest_id in top_destinations:
        dest_name = travel_destinations.loc[
            travel_destinations["Destination_ID"] == dest_id, "Destination_Name"].iloc[0]
        rating_info = test_rating[dest_id]
        recommendations.append({
            "Destination Name": dest_name,
            "Predicted Rating": rating_info["predicted_rating"],
            "Eco Score": rating_info["eco_score"],
            "Combined Score": rating_info["combined_score"],
        })

    return recommendations

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Travel Recommendation API!"})

@app.route('/recommendations', methods=['POST'])
def recommendations():
    try:
        input_data = request.get_json()
        user_id = input_data.get("user_id")
        category_filter = input_data.get("category")

        if not user_id:
            return jsonify({"error": "Missing user_id"}), 400

        if user_id not in user_mapping:
            return jsonify({"error": "Invalid user_id"}), 400

        if category_filter and category_filter not in travel_destinations_df["Category"].unique():
            return jsonify({"error": "Invalid category filter"}), 400

        destination_ids = travel_destinations_df["Destination_ID"].unique()
        recommendations = generate_recommendations(
            interpreter, user_id, destination_ids, travel_destinations_df, category_filter
        )

        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
