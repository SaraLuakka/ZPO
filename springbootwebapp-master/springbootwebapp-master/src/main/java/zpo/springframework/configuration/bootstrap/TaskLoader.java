package zpo.springframework.configuration.bootstrap;

import zpo.springframework.domain.Task;
import zpo.springframework.repositories.TaskRepository;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationListener;
import org.springframework.context.event.ContextRefreshedEvent;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;

@Component
public class TaskLoader implements ApplicationListener<ContextRefreshedEvent> {

    private TaskRepository taskRepository;

    private Logger log = LogManager.getLogger(TaskLoader.class);

    @Autowired
    public void setTaskRepository(TaskRepository taskRepository) {
        this.taskRepository = taskRepository;
    }

    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {

        Task shirt = new Task();
        shirt.setDescription("ABC");
        shirt.setPrice(new BigDecimal("3"));
        shirt.setImageUrl("https://giphy.com/gifs/brownsugarapp-ugh-stressed-stressing-7MDZS8zS1ixtJAUEul");
        shirt.setTaskId("123");
        taskRepository.save(shirt);

        log.info("ABC - id: " + shirt.getId());

        Task mug = new Task();
        mug.setDescription("QWERTY");
        mug.setImageUrl("https://giphy.com/gifs/brownsugarapp-ugh-stressed-stressing-7MDZS8zS1ixtJAUEul");
        mug.setTaskId("000");
        mug.setPrice(new BigDecimal("5"));
        taskRepository.save(mug);

        log.info("QWERTY - id:" + mug.getId());
    }
}

