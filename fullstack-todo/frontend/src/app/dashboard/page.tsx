'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import { useTasks } from '@/hooks/use-tasks';
import TaskCard from '@/components/tasks/task-card';
import LoadingSpinner from '@/components/common/loading-spinner';
import { Task } from '@/types/tasks';
import Link from 'next/link';
import UserMenu from '@/components/auth/user-menu';

export default function DashboardPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const { tasks, loading: tasksLoading, error, fetchTasks, forceRefresh, toggleTaskCompletion, deleteTask } = useTasks(user?.id || '');
  const hasFetchedOnMount = useRef(false);

  // Redirect to login if user is not authenticated, but only after auth loading is complete
  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    }
  }, [authLoading, user, router]);

  // Refresh tasks when the component mounts to ensure fresh data
  useEffect(() => {
    if (user?.id && !hasFetchedOnMount.current) {
      hasFetchedOnMount.current = true;
      forceRefresh();
    }
  }, [user?.id, forceRefresh]);

  if (authLoading) {
    return (
      <div className="p-6">
        <div className="flex justify-center items-center h-64">
          <LoadingSpinner />
        </div>
      </div>
    );
  }

  // If user is not authenticated and not loading, show nothing or loading state
  if (!authLoading && !user) {
    return null; // or show a loading state while redirect happens
  }

  if (tasksLoading && tasks.length === 0) {
    return (
      <div className="p-6">
        <div className="flex justify-center items-center h-64">
          <LoadingSpinner />
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
        <div className="flex items-center space-x-4">
          <Link
            href="/tasks/new"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Add Task
          </Link>
          <UserMenu />
        </div>
      </div>

      {error && (
        <div className="rounded-md bg-red-50 p-4 mb-4">
          <div className="flex">
            <div className="shrink-0">
              <span className="text-red-400">⚠️</span>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error loading tasks</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>{error}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              vectorEffect="non-scaling-stroke"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
          <div className="mt-6">
            <Link
              href="/tasks/new"
              className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Create new task
            </Link>
          </div>
        </div>
      ) : (
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <ul className="divide-y divide-gray-200">
            {tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onToggleComplete={async (id, completed) => {
                  try {
                    await toggleTaskCompletion(id);
                  } catch (error) {
                    console.error('Error toggling task completion:', error);
                    // Fetch tasks to ensure UI is up-to-date
                    fetchTasks();
                  }
                }}
                onEdit={(task) => {
                  // Navigate to edit page
                  window.location.href = `/tasks/${task.id}/edit`;
                }}
                onDelete={async (id) => {
                  try {
                    await deleteTask(id);
                  } catch (error) {
                    console.error('Error deleting task:', error);
                    // Fetch tasks to ensure UI is up-to-date
                    fetchTasks();
                  }
                }}
              />
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}