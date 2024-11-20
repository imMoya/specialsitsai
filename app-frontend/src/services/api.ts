import axios from 'axios';
import { SummaryData, DatasetInfo } from '../types';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const getSummaryData = async (): Promise<SummaryData> => {
  try {
    const [oddlotsResponse, spinoffsResponse] = await Promise.all([
      api.get<DatasetInfo>('/oddlots'),
      api.get<DatasetInfo>('/spinoffs')
    ]);

    return {
      oddlots: oddlotsResponse.data,
      spinoffs: spinoffsResponse.data
    };
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};