package com.manish.project.userservice.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class FeedbackEvent {
    private Long userId;
    private Long itemId;
    private double rating;
}
