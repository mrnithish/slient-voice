import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'entry_result_screen.dart';

class EntryDetailScreen extends StatelessWidget {
  final Map<String, dynamic> entry;

  const EntryDetailScreen({super.key, required this.entry});

  @override
  Widget build(BuildContext context) {
    final emotionData = entry['emotion_data'] as Map<String, dynamic>?;
    final createdAt = DateTime.parse(entry['created_at']);
    final transcript = entry['transcript'] as String?;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Entry Details'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              DateFormat('MMMM dd, yyyy • HH:mm').format(createdAt),
              style: const TextStyle(
                fontSize: 14,
                color: Colors.grey,
              ),
            ),
            const SizedBox(height: 24),
            if (emotionData != null) ...[
              const Text(
                'Emotion Analysis',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16),
              _buildEmotionCard(emotionData),
              const SizedBox(height: 24),
            ],
            if (transcript != null && transcript.isNotEmpty) ...[
              const Text(
                'Transcript',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Text(
                    transcript,
                    style: const TextStyle(fontSize: 16),
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildEmotionCard(Map<String, dynamic> emotionData) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildEmotionRow('Primary Emotion', emotionData['primary_emotion'] ?? 'N/A'),
            if (emotionData['mood_score'] != null)
              _buildEmotionRow('Mood Score', emotionData['mood_score'].toString()),
            _buildEmotionRow('Stress Level', emotionData['stress_level'] ?? 'N/A'),
            _buildEmotionRow('Energy Level', emotionData['energy_level'] ?? 'N/A'),
            _buildEmotionRow('Confidence Level', emotionData['confidence_level'] ?? 'N/A'),
            if (emotionData['summary'] != null) ...[
              const SizedBox(height: 16),
              const Divider(),
              const SizedBox(height: 16),
              Text(
                'Summary',
                style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  color: Colors.grey,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                emotionData['summary'],
                style: const TextStyle(fontSize: 14),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildEmotionRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: const TextStyle(
              fontSize: 14,
              color: Colors.grey,
            ),
          ),
          Text(
            value,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }
}



