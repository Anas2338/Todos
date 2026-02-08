// Service for synchronizing todo data between chat and traditional UI

import { Todo } from '../../types/todo';
import { chatService } from './chatService';
import { CONFIG } from '../../utils/constants';

interface TodoChangeEvent {
  type: 'created' | 'updated' | 'deleted';
  todo: Todo | string; // Todo object for created/updated, ID for deleted
  source: 'chat' | 'traditional';
  timestamp: Date;
}

class TodoSyncService {
  private static instance: TodoSyncService;
  private listeners: Array<(todos: Todo[]) => void> = [];
  private changeListeners: Array<(event: TodoChangeEvent) => void> = [];
  private syncInterval: NodeJS.Timeout | null = null;
  private webSocket: WebSocket | null = null;
  private userId: string | null = null;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;
  private reconnectDelay: number = 1000;

  private constructor() {}

  public static getInstance(): TodoSyncService {
    if (!TodoSyncService.instance) {
      TodoSyncService.instance = new TodoSyncService();
    }
    return TodoSyncService.instance;
  }

  /**
   * Initialize the synchronization service with user ID
   */
  async initialize(userId: string): Promise<void> {
    this.userId = userId;
    await this.connectWebSocket();
  }

  /**
   * Connect to WebSocket for real-time updates
   */
  private connectWebSocket(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        // Use the configured WebSocket URL from constants
        const wsUrl = `${CONFIG.WS_BASE_URL}/ws/todos/${this.userId}`;
        this.webSocket = new WebSocket(wsUrl);

        this.webSocket.onopen = () => {
          console.log('Connected to WebSocket for todo synchronization');
          this.reconnectAttempts = 0;
          resolve();
        };

        this.webSocket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this.handleWebSocketMessage(data);
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        this.webSocket.onerror = (error) => {
          console.error('WebSocket error:', error);
          reject(error);
        };

        this.webSocket.onclose = (event) => {
          console.log('WebSocket connection closed:', event.code, event.reason);

          // Attempt to reconnect if connection was not intentionally closed
          if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);

            setTimeout(() => {
              this.connectWebSocket().catch(err => console.error('Reconnection failed:', err));
            }, this.reconnectDelay * this.reconnectAttempts);
          }
        };
      } catch (error) {
        console.error('Failed to establish WebSocket connection:', error);
        reject(error);
      }
    });
  }

  /**
   * Handle incoming WebSocket messages
   */
  private handleWebSocketMessage(data: any): void {
    if (data.type && data.event) {
      const changeEvent: TodoChangeEvent = {
        type: data.event.type,
        todo: data.event.todo,
        source: data.event.source,
        timestamp: new Date(data.event.timestamp)
      };

      // Notify change listeners
      this.changeListeners.forEach(listener => listener(changeEvent));

      // If the change came from a different source, fetch updated todos
      if (changeEvent.source !== 'chat') {
        this.fetchAndSyncTodos(this.userId!).catch(err =>
          console.error('Error fetching todos after WebSocket event:', err)
        );
      }
    }
  }

  /**
   * Broadcast changes to WebSocket
   */
  private broadcastChange(event: TodoChangeEvent): void {
    if (this.webSocket && this.webSocket.readyState === WebSocket.OPEN) {
      const message = JSON.stringify({
        type: 'todo_change',
        event: {
          type: event.type,
          todo: event.todo,
          source: event.source,
          timestamp: event.timestamp.toISOString()
        }
      });

      this.webSocket.send(message);
    }
  }

  /**
   * Subscribe to todo updates
   * @param callback Function to call when todos are updated
   * @returns Unsubscribe function
   */
  subscribe(callback: (todos: Todo[]) => void): () => void {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter(listener => listener !== callback);
    };
  }

  /**
   * Subscribe to todo change events
   * @param callback Function to call when a todo change occurs
   * @returns Unsubscribe function
   */
  subscribeToChanges(callback: (event: TodoChangeEvent) => void): () => void {
    this.changeListeners.push(callback);
    return () => {
      this.changeListeners = this.changeListeners.filter(listener => listener !== callback);
    };
  }

  /**
   * Notify all subscribers of todo updates
   */
  private notifySubscribers(todos: Todo[]): void {
    this.listeners.forEach(listener => listener(todos));
  }

  /**
   * Notify all change subscribers of todo changes
   */
  private notifyChangeSubscribers(event: TodoChangeEvent): void {
    this.changeListeners.forEach(listener => listener(event));
  }

  /**
   * Sync todos from chat responses to traditional UI
   */
  async syncTodosFromChat(chatTodos: Todo[]): Promise<void> {
    console.log('Syncing todos from chat:', chatTodos);

    // Notify subscribers of the new todos
    this.notifySubscribers(chatTodos);

    // Broadcast the changes to other UIs
    for (const todo of chatTodos) {
      const changeEvent: TodoChangeEvent = {
        type: 'updated', // Could be 'created' if new, 'updated' if existing
        todo: todo,
        source: 'chat',
        timestamp: new Date()
      };

      this.notifyChangeSubscribers(changeEvent);
      this.broadcastChange(changeEvent);
    }
  }

  /**
   * Sync todo changes from traditional UI to chat
   */
  async syncTodosToChat(todoChanges: { created?: Todo[], updated?: Todo[], deleted?: string[] }): Promise<void> {
    console.log('Syncing todo changes to chat:', todoChanges);

    // Handle created todos
    if (todoChanges.created) {
      for (const todo of todoChanges.created) {
        const changeEvent: TodoChangeEvent = {
          type: 'created',
          todo: todo,
          source: 'traditional',
          timestamp: new Date()
        };

        this.notifyChangeSubscribers(changeEvent);
        this.broadcastChange(changeEvent);
      }
    }

    // Handle updated todos
    if (todoChanges.updated) {
      for (const todo of todoChanges.updated) {
        const changeEvent: TodoChangeEvent = {
          type: 'updated',
          todo: todo,
          source: 'traditional',
          timestamp: new Date()
        };

        this.notifyChangeSubscribers(changeEvent);
        this.broadcastChange(changeEvent);
      }
    }

    // Handle deleted todos
    if (todoChanges.deleted) {
      for (const todoId of todoChanges.deleted) {
        const changeEvent: TodoChangeEvent = {
          type: 'deleted',
          todo: todoId,
          source: 'traditional',
          timestamp: new Date()
        };

        this.notifyChangeSubscribers(changeEvent);
        this.broadcastChange(changeEvent);
      }
    }

    // Notify subscribers of all changes
    const allUpdatedTodos = [
      ...(todoChanges.created || []),
      ...(todoChanges.updated || [])
    ];

    if (allUpdatedTodos.length > 0) {
      this.notifySubscribers(allUpdatedTodos);
    }
  }

  /**
   * Fetch todos from backend and sync across UIs
   */
  async fetchAndSyncTodos(userId: string): Promise<Todo[]> {
    try {
      // In a real implementation, this would fetch from the backend
      // For now, we'll return an empty array
      // In a real implementation, this would call the backend API
      const todos: Todo[] = [];

      this.notifySubscribers(todos);
      return todos;
    } catch (error) {
      console.error('Error fetching todos for sync:', error);
      throw error;
    }
  }

  /**
   * Start periodic synchronization as backup to WebSocket
   */
  startPeriodicSync(intervalMs: number = 30000): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
    }

    this.syncInterval = setInterval(async () => {
      try {
        if (this.userId) {
          await this.fetchAndSyncTodos(this.userId);
        }
      } catch (error) {
        console.error('Error during periodic sync:', error);
      }
    }, intervalMs);
  }

  /**
   * Stop periodic synchronization
   */
  stopPeriodicSync(): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
    }
  }

  /**
   * Trigger an immediate sync
   */
  async triggerSync(): Promise<void> {
    console.log('Triggering immediate sync...');
    if (this.userId) {
      await this.fetchAndSyncTodos(this.userId);
    }
  }

  /**
   * Sync state changes from MCP tools execution
   */
  async syncMCPToolResults(toolResults: Array<{
    toolCallId: string;
    result: any;
    status: 'success' | 'error';
    todosAffected: Todo[];
  }>): Promise<void> {
    if (!toolResults || toolResults.length === 0) return;

    // Collect all affected todos
    const allAffectedTodos: Todo[] = [];
    for (const result of toolResults) {
      if (result.todosAffected && result.todosAffected.length > 0) {
        allAffectedTodos.push(...result.todosAffected);

        // Broadcast each affected todo
        for (const todo of result.todosAffected) {
          const changeEvent: TodoChangeEvent = {
            type: 'updated',
            todo: todo,
            source: 'chat',
            timestamp: new Date()
          };

          this.notifyChangeSubscribers(changeEvent);
          this.broadcastChange(changeEvent);
        }
      }
    }

    if (allAffectedTodos.length > 0) {
      // Sync the affected todos to all subscribers
      this.notifySubscribers(allAffectedTodos);
    }
  }

  /**
   * Close the WebSocket connection
   */
  disconnect(): void {
    if (this.webSocket) {
      this.webSocket.close(1000, 'Client disconnected');
      this.webSocket = null;
    }

    if (this.syncInterval) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
    }

    this.userId = null;
  }
}

export const todoSyncService = TodoSyncService.getInstance();