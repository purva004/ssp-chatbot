import { askRAG, checkRAGHealth } from './ragService';
import { askGraph, checkGraphHealth } from './graphService';
import { askCrewAI, checkCrewAIHealth } from './crewaiService';

export type AIServiceType = 'rag' | 'graph' | 'crewai';

export interface AIServiceConfig {
  name: string;
  displayName: string;
  description: string;
  port: number;
  healthCheck: () => Promise<boolean>;
  askFunction: (question: string, model?: string) => Promise<string>;
}

export const AI_SERVICES: Record<AIServiceType, AIServiceConfig> = {
  rag: {
    name: 'rag',
    displayName: 'RAG Chatbot',
    description: 'RAG-based chatbot using FAISS vector search',
    port: 8000,
    healthCheck: checkRAGHealth,
    askFunction: askRAG,
  },
  graph: {
    name: 'graph',
    displayName: 'Graph Chatbot',
    description: 'Graph-based chatbot using Neo4j',
    port: 8000,
    healthCheck: checkGraphHealth,
    askFunction: askGraph,
  },
  crewai: {
    name: 'crewai',
    displayName: 'CrewAI Multi-Agent',
    description: 'Multi-agent system using CrewAI',
    port: 8000,
    healthCheck: checkCrewAIHealth,
    askFunction: (question: string) => askCrewAI(question), // CrewAI doesn't use model parameter
  },
};

export async function askAI(
  question: string,
  serviceType: AIServiceType,
  model?: string
): Promise<string> {
  const service = AI_SERVICES[serviceType];
  if (!service) {
    throw new Error(`Unknown AI service: ${serviceType}`);
  }

  try {
    return await service.askFunction(question, model);
  } catch (error) {
    console.error(`${service.displayName} Error:`, error);
    throw error;
  }
}

export async function checkAIServiceHealth(serviceType: AIServiceType): Promise<boolean> {
  const service = AI_SERVICES[serviceType];
  if (!service) {
    return false;
  }

  try {
    return await service.healthCheck();
  } catch (error) {
    console.error(`${service.displayName} Health Check Error:`, error);
    return false;
  }
}

export async function getAllServiceHealth(): Promise<Record<AIServiceType, boolean>> {
  const healthChecks = await Promise.allSettled(
    Object.keys(AI_SERVICES).map(async (serviceType) => {
      const health = await checkAIServiceHealth(serviceType as AIServiceType);
      return { serviceType: serviceType as AIServiceType, health };
    })
  );

  const result: Record<AIServiceType, boolean> = {
    rag: false,
    graph: false,
    crewai: false,
  };

  healthChecks.forEach((check) => {
    if (check.status === 'fulfilled') {
      result[check.value.serviceType] = check.value.health;
    }
  });

  return result;
}
