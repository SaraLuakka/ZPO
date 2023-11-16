package zpo.springframework.controllers;

import zpo.springframework.domain.Task;
import zpo.springframework.services.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
public class TaskController {

    private TaskService taskService;

    @Autowired
    public void setTaskService(TaskService taskService) {
        this.taskService = taskService;
    }

    @RequestMapping(value = "/tasks", method = RequestMethod.GET)
    public String list(Model model){
        model.addAttribute("tasks", taskService.listAllTasks());
        System.out.println("Returning tasks:");
        return "tasks";
    }

    @RequestMapping("task/{id}")
    public String showTask(@PathVariable Integer id, Model model){
        model.addAttribute("task", taskService.getTaskById(id));
        return "taskshow";
    }

    @RequestMapping("task/edit/{id}")
    public String edit(@PathVariable Integer id, Model model){
        model.addAttribute("task", taskService.getTaskById(id));
        return "taskform";
    }

    @RequestMapping("task/new")
    public String newTask(Model model){
        model.addAttribute("task", new Task());
        return "taskform";
    }

    @RequestMapping(value = "task", method = RequestMethod.POST)
    public String saveTask(Task task){

        taskService.saveTask(task);

        return "redirect:/task/" + task.getId();
    }
}
