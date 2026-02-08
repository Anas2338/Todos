import { Task } from '@/types/tasks';
import Button from '@/components/ui/Button';
import { useState } from 'react';

// Helper function to safely format dates
const formatDate = (dateValue: string | Date | undefined): string => {
  if (!dateValue) {
    return 'Date not available';
  }

  // Handle empty string specifically
  if (typeof dateValue === 'string' && dateValue.trim() === '') {
    return 'Date not available';
  }

  let date: Date | null = null;

  if (typeof dateValue === 'string') {
    // If it's a string, try to parse it
    date = new Date(dateValue);
  } else if (dateValue instanceof Date) {
    // If it's already a Date object
    date = dateValue;
  } else {
    // If it's neither a string nor a Date object
    return 'Date not available';
  }

  // Check if the date is valid
  if (isNaN(date.getTime())) {
    return 'Invalid date';
  }

  // Format as locale date string
  return date.toLocaleDateString();
};

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: string, completed: boolean) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
}

export default function TaskCard({ task, onToggleComplete, onEdit, onDelete }: TaskCardProps) {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      setIsDeleting(true);
      try {
        await onDelete(task.id);
      } catch (error) {
        console.error('Failed to delete task:', error);
        alert('Failed to delete task. Please try again.');
      } finally {
        setIsDeleting(false);
      }
    }
  };

  return (
    <li className="bg-white px-4 py-4 sm:px-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={(e) => onToggleComplete(task.id, e.target.checked)}
            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <div className="ml-3 min-w-0 flex-1">
            <p className={`text-sm font-medium ${task.completed ? 'text-gray-500 line-through' : 'text-gray-900'}`}>
              {task.title}
            </p>
            {task.description && (
              <p className={`text-sm ${task.completed ? 'text-gray-400' : 'text-gray-500'}`}>
                {task.description}
              </p>
            )}
          </div>
        </div>
        <div className="flex space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => onEdit(task)}
          >
            Edit
          </Button>
          <Button
            variant="danger"
            size="sm"
            onClick={handleDelete}
            loading={isDeleting}
          >
            Delete
          </Button>
        </div>
      </div>
      <div className="mt-2 flex items-center justify-between text-xs text-gray-500">
        <span>Created: {formatDate(task.createdAt)}</span>
        {task.completed && (
          <span>Completed: {formatDate(task.updatedAt)}</span>
        )}
      </div>
    </li>
  );
}