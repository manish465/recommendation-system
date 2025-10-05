package com.manish.project.userservice.scheduler;

import com.manish.project.userservice.service.RecommendationService;
import lombok.RequiredArgsConstructor;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.concurrent.TimeUnit;

@Component
@RequiredArgsConstructor
public class RecommenderScheduler {
    private final RecommendationService recommendationService;

    @Scheduled(fixedRate = 5, timeUnit = TimeUnit.MINUTES)
    public void autoRetrain() {
        System.out.println("Triggering model retraining...");
        recommendationService.triggerRetraining();
    }
}
