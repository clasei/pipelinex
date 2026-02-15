import { ChatMessage, HyperParameters, LogEntry } from "./types";

export const INITIAL_PARAMS: HyperParameters = {
  temperature: 0.70,
  topP: 0.95,
  learningRate: "5e-5",
  batchSize: 128,
  epochs: 10,
  useLoRA: true,
  quantization: false,
};

export const INITIAL_MESSAGES: ChatMessage[] = [
  {
    id: '1',
    role: 'user',
    text: 'Analyze the current run. Are we seeing convergence on the new dataset loop?',
  },
  {
    id: '2',
    role: 'assistant',
    text: 'Pipeline analysis complete. Convergence is accelerating on the `hack_v2` subset. Loss decreased by 15% in the last 200 steps. Flow efficiency is high.',
    codeBlock: 'chk_4200',
    metadata: '> flow_metrics: [coherence: 0.92, latency: 42ms, flux: stable]'
  }
];

export const MOCK_LOGS: LogEntry[] = [
  { id: '1', timestamp: '14:22:10', level: 'INFO', message: 'Initializing pipeline optimizer AdamW with lr=5e-5' },
  { id: '2', timestamp: '14:22:12', level: 'INFO', message: 'Loop 3/10 | Step 4200/10000 | Loss: 0.0435 | Flux: 1.04' },
  { id: '3', timestamp: '14:22:15', level: 'INFO', message: 'Loop 3/10 | Step 4210/10000 | Loss: 0.0428 | Flux: 1.04' },
  { id: '4', timestamp: '14:22:18', level: 'PROGRESS', message: '[####----------------] 42% Complete' },
  { id: '5', timestamp: '14:22:20', level: 'INFO', message: 'Loop 3/10 | Step 4220/10000 | Loss: 0.0421 | Flux: 1.03' },
  { id: '6', timestamp: '14:22:22', level: 'WARN', message: 'Gradient surge detected at step 4225' },
  { id: '7', timestamp: '14:22:25', level: 'INFO', message: 'Loop 3/10 | Step 4230/10000 | Loss: 0.0418 | Flux: 1.03' },
];