'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { useAuth } from '@/hooks/use-auth';
import { useTasks } from '@/hooks/use-tasks';
import TaskForm from '@/components/tasks/task-form';
import { CreateTaskData } from '@/types/tasks';

export default function NewTaskPage() {
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();
  const { createTask } = useTasks(user?.id || '');

  // Redirect to login if not authenticated, but only after auth loading is complete
  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    }
  }, [authLoading, user, router]);

  // If user is not authenticated and not loading, show nothing or loading state
  if (!authLoading && !user) {
    return null; // or show a loading state while redirect happens
  }

  const handleSubmit = async (taskData: CreateTaskData) => {
    if (user) {
      try {
        // Create the task
        await createTask(taskData);

        // Slightly longer delay to ensure task is saved in backend before redirecting
        await new Promise(resolve => setTimeout(resolve, 500));

        // Redirect to dashboard
        router.push('/dashboard');
      } catch (error) {
        console.error('Error creating task:', error);
        // The error is already handled by the useTasks hook in the error state
        // We could add additional error handling here if needed
      }
    }
  };

  const handleCancel = () => {
    router.push('/dashboard');
  };

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Create New Task</h1>
      <TaskForm
        onSubmit={handleSubmit}
        onCancel={handleCancel}
        submitButtonText="Create Task"
      />
    </div>
  );
}