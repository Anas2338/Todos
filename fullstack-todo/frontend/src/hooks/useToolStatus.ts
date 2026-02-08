// Custom hook for tracking tool execution status in ChatKit integration

import { useState, useCallback } from 'react';
import { ToolExecutionState } from '../types/chat';

const useToolStatus = () => {
  const [toolState, setToolState] = useState<ToolExecutionState>({
    activeToolCalls: [],
    showNotifications: true,
  });

  const startToolCall = useCallback((id: string, name: string) => {
    setToolState(prev => ({
      ...prev,
      activeToolCalls: [
        ...prev.activeToolCalls,
        {
          id,
          name,
          status: 'pending',
          startTime: new Date(),
        }
      ]
    }));
  }, []);

  const updateToolStatus = useCallback((id: string, status: 'pending' | 'executing' | 'completed' | 'failed', result?: any) => {
    setToolState(prev => ({
      ...prev,
      activeToolCalls: prev.activeToolCalls.map(call =>
        call.id === id
          ? {
              ...call,
              status,
              result: result !== undefined ? result : call.result
            }
          : call
      )
    }));
  }, []);

  const completeToolCall = useCallback((id: string, result?: any) => {
    updateToolStatus(id, 'completed', result);
  }, [updateToolStatus]);

  const failToolCall = useCallback((id: string, result?: any) => {
    updateToolStatus(id, 'failed', result);
  }, [updateToolStatus]);

  const removeToolCall = useCallback((id: string) => {
    setToolState(prev => ({
      ...prev,
      activeToolCalls: prev.activeToolCalls.filter(call => call.id !== id)
    }));
  }, []);

  const clearAllToolCalls = useCallback(() => {
    setToolState(prev => ({
      ...prev,
      activeToolCalls: []
    }));
  }, []);

  const getToolCall = useCallback((id: string) => {
    return toolState.activeToolCalls.find(call => call.id === id);
  }, [toolState.activeToolCalls]);

  const toggleNotifications = useCallback(() => {
    setToolState(prev => ({
      ...prev,
      showNotifications: !prev.showNotifications
    }));
  }, []);

  return {
    ...toolState,
    startToolCall,
    updateToolStatus,
    completeToolCall,
    failToolCall,
    removeToolCall,
    clearAllToolCalls,
    getToolCall,
    toggleNotifications,
  };
};

export default useToolStatus;