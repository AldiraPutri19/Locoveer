import jwt from "jsonwebtoken";

export const verifyToken = (req, res, next) => {
    const authHeader = req.headers['authorization']; 
    console.log(authHeader)
    const token = authHeader
    
    if (token == null) {
        return res.status(401).json({ msg: "Token tidak ditemukan" }); 
    }

    jwt.verify(token, process.env.ACCESS_TOKEN_SECRET, (err, decoded) => {
        if (err) {
            return res.status(403).json({ msg: "Token tidak valid" }); 
        }

        req.email = decoded.email; 
        next(); 
    });
};
