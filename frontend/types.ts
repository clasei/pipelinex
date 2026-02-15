export interface LogEntry {
  id: string;
  timestamp: string;
  level: 'INFO' | 'WARN' | 'ERROR' | 'PROGRESS';
  message: string;
  metadata?: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  metadata?: string; // For extra info like benchmark results
  codeBlock?: string; // Highlighted text
}

export interface TrainingStats {
  epoch: number;
  totalEpochs: number;
  step: number;
  totalSteps: number;
  loss: number;
  perplexity: number;
  throughput: number; // tokens per sec
}

export interface HyperParameters {
  temperature: number;
  topP: number;
  learningRate: string;
  batchSize: number;
  epochs: number;
  useLoRA: boolean;
  quantization: boolean;
}
