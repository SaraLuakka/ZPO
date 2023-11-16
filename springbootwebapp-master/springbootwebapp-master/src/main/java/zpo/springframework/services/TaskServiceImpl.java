package zpo.springframework.services;

import zpo.springframework.domain.Task;
import zpo.springframework.repositories.TaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TaskServiceImpl implements TaskService {
    private TaskRepository taskRepository;

    @Autowired
    public void setTaskRepository(TaskRepository taskRepository) {
        this.taskRepository = taskRepository;
    }

    @Override
    public Iterable<Task> listAllTasks() {
        return taskRepository.findAll();
    }

    @Override
    public Task getTaskById(Integer id) {
        return taskRepository.findById(id).orElse(null);
    }

    @Override
    public Task saveTask(Task task) {
        return taskRepository.save(task);
    }

    @Override
    public Iterable<Task> listAllProducts() {
        return null;
    }

    @Override
    public Task getProductById(Integer id) {
        return null;
    }

    @Override
    public Task saveProduct(Task task) {
        return null;
    }
}
