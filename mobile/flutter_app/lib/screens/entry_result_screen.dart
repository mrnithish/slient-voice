import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class EntryResultScreen extends StatelessWidget {
  final Map<String, dynamic> entry;

  const EntryResultScreen({super.key, required this.entry});

  @override
  Widget build(BuildContext context) {
    final emotionData = entry['emotion_data'] as Map<String, dynamic>?;
    
    if (emotionData == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('Analysis Result')),
        body: const Center(
          child: Text('No emotion data available'),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Emotion Analysis'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildSection(
              'Primary Emotion',
              emotionData['primary_emotion'] ?? 'N/A',
            ),
            const SizedBox(height: 24),
            _buildMoodScore(emotionData['mood_score'] ?? 0),
            const SizedBox(height: 24),
            _buildSection(
              'Stress Level',
              emotionData['stress_level'] ?? 'N/A',
            ),
            const SizedBox(height: 24),
            if (emotionData['secondary_emotions'] != null &&
                (emotionData['secondary_emotions'] as List).isNotEmpty)
              _buildListSection(
                'Secondary Emotions',
                List<String>.from(emotionData['secondary_emotions']),
              ),
            const SizedBox(height: 24),
            if (emotionData['themes'] != null &&
                (emotionData['themes'] as List).isNotEmpty)
              _buildListSection(
                'Themes',
                List<String>.from(emotionData['themes']),
              ),
            const SizedBox(height: 24),
            _buildSection(
              'Energy Level',
              emotionData['energy_level'] ?? 'N/A',
            ),
            const SizedBox(height: 24),
            _buildSection(
              'Confidence Level',
              emotionData['confidence_level'] ?? 'N/A',
            ),
            const SizedBox(height: 24),
            if (emotionData['summary'] != null)
              _buildSection(
                'Summary',
                emotionData['summary'],
                isLarge: true,
              ),
            const SizedBox(height: 32),
            ElevatedButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 48),
              ),
              child: const Text('Done'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSection(String title, String content, {bool isLarge = false}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.bold,
            color: Colors.grey,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          content,
          style: TextStyle(
            fontSize: isLarge ? 16 : 18,
            fontWeight: isLarge ? FontWeight.normal : FontWeight.w500,
          ),
        ),
      ],
    );
  }

  Widget _buildMoodScore(int score) {
    final color = score < 0
        ? Colors.red
        : score > 0
            ? Colors.green
            : Colors.grey;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Mood Score',
          style: TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.bold,
            color: Colors.grey,
          ),
        ),
        const SizedBox(height: 8),
        Row(
          children: [
            Text(
              score.toString(),
              style: TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: LinearProgressIndicator(
                value: (score + 5) / 10,
                backgroundColor: Colors.grey[300],
                valueColor: AlwaysStoppedAnimation<Color>(color),
                minHeight: 8,
              ),
            ),
          ],
        ),
        const SizedBox(height: 4),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: const [
            Text('-5', style: TextStyle(fontSize: 12, color: Colors.grey)),
            Text('0', style: TextStyle(fontSize: 12, color: Colors.grey)),
            Text('+5', style: TextStyle(fontSize: 12, color: Colors.grey)),
          ],
        ),
      ],
    );
  }

  Widget _buildListSection(String title, List<String> items) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.bold,
            color: Colors.grey,
          ),
        ),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: items.map((item) {
            return Chip(
              label: Text(item),
              backgroundColor: Colors.blue[50],
            );
          }).toList(),
        ),
      ],
    );
  }
}



