import axios, { AxiosInstance } from 'axios'
import { useAuthStore } from '../store/authStore'
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  FlightPredictionRequest,
  FlightPredictionResponse,
  GenderPredictionRequest,
  GenderPredictionResponse,
  HotelRecommendationRequest,
  HotelRecommendationResponse,
  PredictionRecord,
  UserStats,
  ApiResponse,
} from '../types'

const API_BASE_URL = 'http://localhost:8000/v1'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add token to requests
    this.client.interceptors.request.use((config) => {
      const token = useAuthStore.getState().token
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Handle responses
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          useAuthStore.getState().logout()
        }
        return Promise.reject(error)
      }
    )
  }

  // Auth endpoints
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/auth/login', credentials)
    return response.data
  }

  async register(data: RegisterRequest): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/auth/register', data)
    return response.data
  }

  async getCurrentUser(): Promise<ApiResponse<any>> {
    const response = await this.client.get<ApiResponse<any>>('/auth/me')
    return response.data
  }

  // Flight prediction endpoints
  async predictFlightPrice(request: FlightPredictionRequest): Promise<FlightPredictionResponse> {
    const response = await this.client.post<FlightPredictionResponse>('/predict', request)
    return response.data
  }

  async getFlightHistory(): Promise<PredictionRecord[]> {
    const response = await this.client.get<PredictionRecord[]>('/predictions/flight')
    return response.data
  }

  // Gender prediction endpoints
  async predictGender(request: GenderPredictionRequest): Promise<GenderPredictionResponse> {
    const response = await this.client.post<GenderPredictionResponse>('/predict-gender', request)
    return response.data
  }

  async getGenderHistory(): Promise<PredictionRecord[]> {
    const response = await this.client.get<PredictionRecord[]>('/predictions/gender')
    return response.data
  }

  // History endpoints
  async getPredictionHistory(limit: number = 50): Promise<PredictionRecord[]> {
    const response = await this.client.get<PredictionRecord[]>('/predictions', {
      params: { limit },
    })
    return response.data
  }

  // Stats endpoints
  async getUserStats(): Promise<UserStats> {
    const response = await this.client.get<UserStats>('/stats')
    return response.data
  }

  // Hotel recommendation endpoints
  async recommendHotels(request: HotelRecommendationRequest): Promise<HotelRecommendationResponse> {
    const response = await this.client.post<HotelRecommendationResponse>('/recommend-hotels', request)
    return response.data
  }

  // Health check
  async healthCheck(): Promise<ApiResponse<any>> {
    const response = await this.client.get<ApiResponse<any>>('/health')
    return response.data
  }
}

export const apiClient = new ApiClient()
