package zpo.springframework.configuration;

import org.h2.util.Task;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;

import javax.persistence.*;
import java.util.Collection;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String username;
    private String password;
    private String email;

    private String name;
    //private List<Task> assignedTasks;
    private int overallRating;

    public String getUsername() {
        return this.username;
    }


    public String getPassword() {
        return this.password;
    }

    public Long getId() {
        return this.id;
    }
    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "user_roles", joinColumns = @JoinColumn(name = "user_id"))
    @Column(name = "role")
    private Set<String> roles = new HashSet<>();

    // Metoda zwracająca role użytkownika jako kolekcję Stringów
    public Set<String> getRoles() {
        return roles;
    }

    // Metoda zwracająca role użytkownika jako obiekty GrantedAuthority
    public Collection<? extends GrantedAuthority> getAuthorities() {
        Set<GrantedAuthority> authorities = new HashSet<>();
        for (String role : roles) {
            authorities.add(new SimpleGrantedAuthority(role));
        }
        return authorities;
    }

    // Getters, setters, etc.
}
