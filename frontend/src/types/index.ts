// Auth Types
export interface User {
  id: string
  email: string
  name: string
  role: 'user' | 'admin'
  created_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  name: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

// Prediction Types

// Flight Price Prediction
export interface FlightPredictionRequest {
  flightType: 'economic' | 'firstClass' | 'premium'
  agency: 'Rainbow' | 'CloudFy' | 'FlyingDrops'
  gender: 'male' | 'female'
  distance: number
  time: number
  age: number
}

export interface FlightPredictionResponse {
  predicted_price: number
}

// Gender Prediction
export interface GenderPredictionRequest {
  flight_count: number
  total_price: number
  total_distance: number
  total_hotel_spend: number
  total_days: number
  age: number
}

export interface GenderPredictionResponse {
  predicted_gender: string
}

// Prediction History
export interface PredictionRecord {
  id: string
  user_id: string
  model_type: 'flight' | 'gender'
  input_data: Record<string, unknown>
  output: FlightPredictionResponse | GenderPredictionResponse
  created_at: string
}

// API Response
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

// Stats
export interface UserStats {
  total_predictions: number
  flight_predictions: number
  gender_predictions: number
  avg_prediction_time_ms: number
  last_prediction: string | null
}

export interface ModelMetrics {
  model_name: string
  model_version: string
  accuracy?: number
  predictions_count: number
  avg_confidence: number
  last_updated: string
}

// Hotel Recommendation Types
export interface HotelRecommendationRequest {
  days: number
  month: number
  age: number
  gender: 'male' | 'female' | 'unknown'
  budget: 'budget' | 'mid' | 'luxury'
  company: '4You' | 'Acme Factory' | 'Monsters CYA' | 'Umbrella LTDA' | 'Wonka Company'
  top_n?: number
}

export interface HotelRecommendation {
  rank: number
  hotel: string
  match_score: number
}

export interface HotelRecommendationResponse {
  recommendations: HotelRecommendation[]
  total_recommendations: number
}
