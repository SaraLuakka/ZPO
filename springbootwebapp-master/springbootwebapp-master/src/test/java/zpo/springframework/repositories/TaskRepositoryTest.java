package zpo.springframework.repositories;

import zpo.springframework.configuration.RepositoryConfiguration;
import zpo.springframework.domain.Task;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.math.BigDecimal;

import static org.junit.Assert.*;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest(classes = {RepositoryConfiguration.class})
public class TaskRepositoryTest {

    private TaskRepository taskRepository;

    @Autowired
    public void setTaskRepository(TaskRepository taskRepository) {
        this.taskRepository = taskRepository;
    }

    @Test
    public void testSaveTask(){
        //setup task
        Task task = new Task();
        task.setDescription("ABC");
        task.setPrice(new BigDecimal("333"));
        task.setTaskId("1234");

        //save task, verify has ID value after save
        assertNull(task.getId()); //null before save
        taskRepository.save(task);
        assertNotNull(task.getId()); //not null after save
        //fetch from DB
        Task fetchedTask = taskRepository.findById(task.getId()).orElse(null);

        //should not be null
        assertNotNull(fetchedTask);

        //should equal
        assertEquals(task.getId(), fetchedTask.getId());
        assertEquals(task.getDescription(), fetchedTask.getDescription());

        //update description and save
        fetchedTask.setDescription("New Description");
        taskRepository.save(fetchedTask);

        //get from DB, should be updated
        Task fetchedUpdatedTask = taskRepository.findById(fetchedTask.getId()).orElse(null);
        assertEquals(fetchedTask.getDescription(), fetchedUpdatedTask.getDescription());

        //verify count of tasks in DB
        long taskCount = taskRepository.count();
        assertEquals(taskCount, 1);

        //get all tasks, list should only have one
        Iterable<Task> tasks = taskRepository.findAll();

        int count = 0;

        for(Task t : tasks){
            count++;
        }

        assertEquals(count, 1);
    }
}
