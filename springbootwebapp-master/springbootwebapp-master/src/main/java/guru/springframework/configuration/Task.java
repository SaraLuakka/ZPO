package guru.springframework.configuration;

import guru.springframework.configuration.TaskCategory;
import guru.springframework.configuration.User;

public class Task {
    private Long id;
    private String name;
    private String description;
    private TaskCategory category;
    private User assignedEmployee;
    private int rating;
    // ... inne pola, gettery, settery
}



//public class Employee {
//    private Long id;
//    private String name;
//    private List<Task> assignedTasks;
//    private int overallRating;
//    // ... inne pola, gettery, settery
//}
