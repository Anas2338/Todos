import { useState, ChangeEvent } from 'react';
import { validateTaskForm } from '@/lib/utils/validation';
import { Task } from '@/types/tasks';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/input';

interface TaskFormProps {
  task?: Task;
  onSubmit: (task: { title: string; description?: string }) => void;
  onCancel?: () => void;
  submitButtonText?: string;
}

export default function TaskForm({ task, onSubmit, onCancel, submitButtonText = 'Save Task' }: TaskFormProps) {
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  const [errors, setErrors] = useState<{ title?: string; description?: string }>({});
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    // Validate form
    const validation = validateTaskForm(title, description);
    if (!validation.isValid) {
      const newErrors: { title?: string; description?: string } = {};
      validation.errors.forEach(err => {
        if (err.includes('title')) {
          newErrors.title = err;
        } else if (err.includes('description')) {
          newErrors.description = err;
        }
      });
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    try {
      onSubmit({ title, description: description || undefined });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Input
          label="Title"
          id="task-title"
          name="title"
          type="text"
          value={title}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setTitle(e.target.value)}
          required
          error={errors.title}
          placeholder="Task title"
        />
      </div>

      <div>
        <Input
          label="Description"
          id="task-description"
          name="description"
          as="textarea"
          rows={4}
          value={description}
          onChange={(e: ChangeEvent<HTMLTextAreaElement>) => setDescription(e.target.value)}
          error={errors.description}
          placeholder="Task description (optional)"
        />
      </div>

      <div className="flex space-x-3">
        <Button type="submit" loading={loading}>
          {submitButtonText}
        </Button>
        {onCancel && (
          <Button type="button" variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
}