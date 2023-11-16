package zpo.springframework.services;


import zpo.springframework.domain.Task;

public interface TaskService {
    Iterable<Task> listAllTasks();

    Task getTaskById(Integer id);

    Task saveTask(Task task);

    Iterable<Task> listAllProducts();

    Task getProductById(Integer id);

    Task saveProduct(Task task);
}
