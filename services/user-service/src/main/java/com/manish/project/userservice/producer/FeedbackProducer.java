package com.manish.project.userservice.producer;

import lombok.RequiredArgsConstructor;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class FeedbackProducer {
    private static final String TOPIC = "feedback-events";
    private final KafkaTemplate<String, String> kafkaTemplate;

    public void sendFeedback(Long userId, Long itemId) {
        String message = userId + "," + itemId;
        kafkaTemplate.send(TOPIC, message);
        System.out.println("Sent feedback event: " + message);
    }
}
