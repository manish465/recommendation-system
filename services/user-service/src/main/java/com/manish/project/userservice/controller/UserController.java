package com.manish.project.userservice.controller;

import com.manish.project.userservice.model.Product;
import com.manish.project.userservice.producer.FeedbackProducer;
import com.manish.project.userservice.service.RecommendationService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/users")
@RequiredArgsConstructor
public class UserController {
    private final RecommendationService recommendationService;
    private final FeedbackProducer feedbackProducer;

    @GetMapping("/{id}/recommendations")
    public List<Product> getUserRecommendations(@PathVariable int id,
                                                @RequestParam(defaultValue = "5") int k) {
        List<Integer> productIds = recommendationService.getRecommendationsForUser(id, k);
        return productIds.stream()
                .map(pid -> new Product(pid, "Product-" + pid, "Demo product"))
                .collect(Collectors.toList());
    }

    @PostMapping("/{userId}/feedback")
    public ResponseEntity<String> sendFeedback(
            @PathVariable Long userId,
            @RequestParam Long itemId) {

        feedbackProducer.sendFeedback(userId, itemId);
        return ResponseEntity.ok("Feedback sent to RecommenderService");
    }

    @PostMapping("/retrain")
    public ResponseEntity<String> retrainModel() {
        recommendationService.triggerRetraining();
        return ResponseEntity.ok("Retraining triggered");
    }
}
