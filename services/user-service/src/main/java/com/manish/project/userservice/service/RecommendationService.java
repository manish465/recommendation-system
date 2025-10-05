package com.manish.project.userservice.service;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

@Service
@RequiredArgsConstructor
public class RecommendationService {
    private final RestTemplate restTemplate;
    private final RedisTemplate<String, Object> redisTemplate;

    @Value("${recommender.api.url}")
    private String recommenderApiUrl;

    public List<Integer> getRecommendationsForUser(int userId, int k) {
        String cacheKey = "user:" + userId + ":recommendations:" + k;
        // Check cache
        List<Integer> cached = (List<Integer>) redisTemplate.opsForValue().get(cacheKey);
        if (cached != null) {
            System.out.println("Cache HIT for user " + userId);
            return cached;
        }

        // Call recommender if not cached
        String url = String.format("%s/recommend?user_id=%d&k=%d", recommenderApiUrl, userId, k);
        Map<String, Object> response = restTemplate.getForObject(url, Map.class);
        List<Integer> recommendations = (List<Integer>) response.get("recommendations");

        // Cache for 1 hour
        redisTemplate.opsForValue().set(cacheKey, recommendations, 1, TimeUnit.HOURS);

        System.out.println("Cache MISS for user " + userId);
        return recommendations;
    }
}
