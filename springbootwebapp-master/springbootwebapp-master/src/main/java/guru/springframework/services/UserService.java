package guru.springframework.services;

import guru.springframework.configuration.User;
import guru.springframework.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

// Serwis do obsługi logiki związanej z użytkownikami
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    public User getUserByIdAndUsername(Long id, String username) {
        return userRepository.findByIdAndUsername(id, username);
    }
}
