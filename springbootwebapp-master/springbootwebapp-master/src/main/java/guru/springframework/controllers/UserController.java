package guru.springframework.controllers;

import guru.springframework.configuration.User;
import guru.springframework.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.nio.file.AccessDeniedException;
import java.security.Principal;

@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserRepository userRepository;

    @GetMapping("/{userId}")
    public User getUserData(@PathVariable Long userId, Principal principal) throws AccessDeniedException {
        String username = principal.getName(); // Nazwa użytkownika zalogowanego
        User loggedInUser = userRepository.findByUsername(username);

        if (loggedInUser.getId().equals(userId)) {
            // Pobieranie danych tylko dla zalogowanego użytkownika
            return loggedInUser;
        } else {
            // Obsługa błędu dostępu do danych innego użytkownika
            throw new AccessDeniedException("Access denied.");
        }
    }
}
