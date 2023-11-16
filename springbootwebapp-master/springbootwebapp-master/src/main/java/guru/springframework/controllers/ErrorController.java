package guru.springframework.controllers;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

import javax.servlet.RequestDispatcher;
import javax.servlet.http.HttpServletRequest;

@Controller
public class ErrorController implements org.springframework.boot.web.servlet.error.ErrorController {

    @RequestMapping("/error")
    public String handleError(HttpServletRequest request) {
        // Pobierz atrybut statusu błędu HTTP
        Object status = request.getAttribute(RequestDispatcher.ERROR_STATUS_CODE);

        if (status != null) {
            int statusCode = Integer.parseInt(status.toString());

            // Obsłuż różne kody błędów i zwróć odpowiedni widok
            if (statusCode == HttpStatus.NOT_FOUND.value()) {
                return "error-404"; // Twój widok dla błędu 404
            } else if (statusCode == HttpStatus.INTERNAL_SERVER_ERROR.value()) {
                return "error-500"; // Twój widok dla błędu 500
            }
            // ... Obsługa innych kodów błędów
        }
        return "error"; // Domyślny widok błędu
    }

    @Override
    public String getErrorPath() {
        return "/error";
    }
}
