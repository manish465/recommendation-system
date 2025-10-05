package com.manish.project.userservice.producer;

import com.manish.project.userservice.model.FeedbackEvent;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class FeedbackProducer {
    private final KafkaTemplate<String, FeedbackEvent> kafkaTemplate;

    @Value("${app.kafka.topic.feedback}")
    private String feedbackTopic;

    public void sendFeedback(FeedbackEvent event) {
        kafkaTemplate.send(feedbackTopic, event);
        System.out.println("Sent feedback event");
    }
}
