# Eenvoudige analyse: Slaapscore vs Hartslag Overdag

library(ggplot2)

# Data laden
sleep_data <- read.csv("/Users/robinoffringa/Desktop/Takeout/Fitbit/Sleep Score/sleep_score.csv")
heartrate_data <- read.csv("/Users/robinoffringa/Desktop/Takeout/Fitbit/average_heart_rate_excluding_sleep.csv")

# Data voorbereiden
sleep_data$date <- as.Date(sleep_data$timestamp)
heartrate_data$date <- as.Date(heartrate_data$date)

# Merge
data <- merge(sleep_data[, c("date", "overall_score", "resting_heart_rate")], 
              heartrate_data[, c("date", "average_heart_rate")], 
              by = "date")
data <- data[complete.cases(data), ]

# Statistieken
cat("=== SLAAPSCORE vs HARTSLAG OVERDAG ===\n\n")

cat("Data punten: n =", nrow(data), "\n\n")

# Beschrijvend
cat("Slaapscore - Mean:", round(mean(data$overall_score), 2), 
    ", SD:", round(sd(data$overall_score), 2), "\n")
cat("Hartslag - Mean:", round(mean(data$average_heart_rate), 2), 
    ", SD:", round(sd(data$average_heart_rate), 2), "\n\n")

# Correlatie - ONE-TAILED (richting: lagere hartslag = hogere score)
corr <- cor.test(data$overall_score, data$average_heart_rate, alternative = "less")
cat("p =", round(corr$p.value, 3), "\n\n")

# Regressie
model <- lm(overall_score ~ average_heart_rate, data = data)
summary(model)

# Plot
png("/Users/robinoffringa/Desktop/Takeout/Fitbit/slaap_hartslag_plot.png", 
    width = 700, height = 500)
p <- ggplot(data, aes(x = average_heart_rate, y = overall_score)) +
  geom_point(size = 4, color = "blue", alpha = 0.7) +
  geom_smooth(method = "lm", color = "red") +
  labs(title = "Slaapscore vs Hartslag Overdag",
       x = "Gemiddelde Hartslag (bpm)",
       y = "Slaapscore")
print(p)
dev.off()

cat("\n✓ Plot opgeslagen: slaap_hartslag_plot.png\n")

# Rusthartslag
cat("\n=== RUSTHARTSLAG ===\n\n")
corr2 <- cor.test(data$overall_score, data$resting_heart_rate, alternative = "less")
cat("p =", round(corr2$p.value, 3), "\n\n")

model2 <- lm(overall_score ~ resting_heart_rate, data = data)
summary(model2)

png("/Users/robinoffringa/Desktop/Takeout/Fitbit/slaap_rusthartslag_plot.png", 
    width = 700, height = 500)
p2 <- ggplot(data, aes(x = resting_heart_rate, y = overall_score)) +
  geom_point(size = 4, color = "darkgreen", alpha = 0.7) +
  geom_smooth(method = "lm", color = "red") +
  labs(title = "Slaapscore vs Rusthartslag",
       x = "Rusthartslag (bpm)",
       y = "Slaapscore")
print(p2)
dev.off()

cat("\n✓ Plot opgeslagen: slaap_rusthartslag_plot.png\n")
