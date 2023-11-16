package zpo.springframework.repositories;

import zpo.springframework.domain.Task;
import org.springframework.data.repository.CrudRepository;

public interface TaskRepository extends CrudRepository<Task, Integer>{
}
