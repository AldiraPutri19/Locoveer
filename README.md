# Locoveer Travel Recommendation System  

## About This Project  

The Locoveer Travel Recommendation System helps users discover travel destinations they’ll love by using advanced machine learning techniques. The system also promotes sustainable tourism by factoring in eco-scores, which highlight destinations with environmentally friendly practices.  

By combining user preferences with sustainability data, this system provides recommendations that align with personal interests and encourage eco-friendly travel.  

---  

## How It Works  

- **Personalized Recommendations**: Suggests destinations based on user preferences and past behavior.  
- **Eco-Friendly Focus**: Integrates sustainability metrics like renewable energy usage, waste management, and cultural preservation.  
- **Collaborative Filtering**: Uses machine learning to predict user preferences based on similar users and destinations.  

---  

## What’s Inside  

```plaintext  
.
├── datasets/
│   ├── eco_impact_matrix.csv
│   ├── travel_destinations.csv
│   ├── user_ratings.csv
│   └── users.csv
├── notebooks/
│   ├── Collaborative_Filtering_Recommendation_System.ipynb
│   ├── Content_Based_Filtering_Recommendation_System.ipynb               # Unfinished Model
├── collaborative_filtering_recommendation_system.keras
├── collaborative_filtering_recommendation_system.tflite
└── README.md
```  

---  

## About the Datasets  

- **Eco-Impact Matrix (`eco_impact_matrix.csv`)**:  
  This dataset provides sustainability scores for each destination. It includes metrics such as:  
  - Renewable energy usage  
  - Waste management systems  
  - Eco-friendliness scores  
  - Accessibility to public transportation  
  - Cultural preservation efforts  
  The data is normalized to ensure compatibility with the recommendation model.  

- **Travel Destinations (`travel_destinations.csv`)**:  
  Includes details about Indonesian tourism destinations, such as names, descriptions, and categories.  

- **User Ratings (`user_ratings.csv`)**:  
  Contains user IDs, destination IDs, and their corresponding ratings. This dataset forms the basis for collaborative filtering.  

- **Users (`users.csv`)**:  
  Contains data about users, such as demographics or unique identifiers, to personalize recommendations.  

---  

## How to Use It  

### Step 1: Install Required Tools  
Make sure you have Python 3.8+ installed, then add these packages:  
```bash  
pip install tensorflow-recommenders tensorflow-datasets pandas matplotlib seaborn
```  

### Step 2: Run the Notebook  
- Open `Collaborative_Filtering_Recommendation_System.ipynb` in Jupyter Notebook or Google Colab.  
- Follow the steps to clean data, train the model, and see recommendations.  

### Step 3: Save or Use the Model  
- The trained model is already saved in two formats:  
  - **Keras**: For further training or debugging.  
  - **TFLite**: For lightweight deployment.  

---  

## References  

1. This project uses the **[Indonesia Tourism Destination dataset](https://www.kaggle.com/datasets/aprabowo/indonesia-tourism-destination)** as the base for `travel_destinations.csv`.  
2. The recommendation system is inspired by the guide ["How to Build a Recommender System using TensorFlow"](https://www.sabrepc.com/blog/Deep-Learning-and-AI/How-to-Build-a-Recommender-System-using-TensorFlow).  

---  

## Collaborators  

- **[Albertus Magnus Foresta Noventona]**  
- **[Dea Putri Nurwahyunita]**  
- **[Hoirul Amin]**   
