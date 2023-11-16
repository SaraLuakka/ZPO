package guru.springframework.repositories;

import guru.springframework.configuration.User;
import org.springframework.data.jpa.repository.JpaRepository;

// Przykład z użyciem Spring Data JPA
public interface UserRepository extends JpaRepository<User, Long> {
    User findByIdAndUsername(Long id, String username);

    User findByUsername(String username);
}
