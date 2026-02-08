import { z } from 'zod';

export const taskSchema = z.object({
  title: z.string()
    .min(1, 'Task title is required')
    .max(100, 'Task title must be 100 characters or less'),
  description: z.string()
    .max(1000, 'Task description must be 1000 characters or less')
    .optional(),
});

export const updateTaskSchema = z.object({
  title: z.string()
    .min(1, 'Task title is required')
    .max(100, 'Task title must be 100 characters or less')
    .optional(),
  description: z.string()
    .max(1000, 'Task description must be 1000 characters or less')
    .optional(),
  completed: z.boolean().optional(),
});

export type TaskFormData = z.infer<typeof taskSchema>;
export type UpdateTaskFormData = z.infer<typeof updateTaskSchema>;