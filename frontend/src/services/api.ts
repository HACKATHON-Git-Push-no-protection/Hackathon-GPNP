import axios from "axios";
import { LogEntry } from "../types/logTypes";

// Define API base URL
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

export const fetchLogs = async (): Promise<LogEntry[]> => {
  try {
    const response = await axios.get<{ logs: LogEntry[] }>(`${API_URL}/logs`);
    return response.data.logs;
  } catch (error) {
    console.error("Error fetching logs:", error);
    throw error;
  }
};
