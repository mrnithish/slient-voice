import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../services/api_service.dart';
import 'entry_detail_screen.dart';

class TimelineScreen extends StatefulWidget {
  const TimelineScreen({super.key});

  @override
  State<TimelineScreen> createState() => _TimelineScreenState();
}

class _TimelineScreenState extends State<TimelineScreen> {
  List<Map<String, dynamic>> _entries = [];
  bool _isLoading = true;
  bool _hasError = false;

  @override
  void initState() {
    super.initState();
    _loadEntries();
  }

  Future<void> _loadEntries() async {
    setState(() {
      _isLoading = true;
      _hasError = false;
    });

    try {
      final apiService = Provider.of<ApiService>(context, listen: false);
      final entries = await apiService.getVoiceEntries();
      
      setState(() {
        _entries = entries;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _hasError = true;
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: RefreshIndicator(
        onRefresh: _loadEntries,
        child: _isLoading
            ? const Center(child: CircularProgressIndicator())
            : _hasError
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.error_outline, size: 64, color: Colors.grey),
                        const SizedBox(height: 16),
                        const Text('Failed to load entries'),
                        const SizedBox(height: 16),
                        ElevatedButton(
                          onPressed: _loadEntries,
                          child: const Text('Retry'),
                        ),
                      ],
                    ),
                  )
                : _entries.isEmpty
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Icon(Icons.mic_none, size: 64, color: Colors.grey),
                            const SizedBox(height: 16),
                            const Text(
                              'No entries yet',
                              style: TextStyle(fontSize: 18, color: Colors.grey),
                            ),
                            const SizedBox(height: 8),
                            const Text(
                              'Start recording to create your first entry',
                              style: TextStyle(fontSize: 14, color: Colors.grey),
                            ),
                          ],
                        ),
                      )
                    : ListView.builder(
                        itemCount: _entries.length,
                        itemBuilder: (context, index) {
                          final entry = _entries[index];
                          final emotionData = entry['emotion_data'] as Map<String, dynamic>?;
                          final createdAt = DateTime.parse(entry['created_at']);

                          return Card(
                            margin: const EdgeInsets.symmetric(
                              horizontal: 16,
                              vertical: 8,
                            ),
                            child: ListTile(
                              leading: CircleAvatar(
                                backgroundColor: _getEmotionColor(emotionData?['primary_emotion']),
                                child: const Icon(Icons.mic, color: Colors.white),
                              ),
                              title: Text(
                                emotionData?['primary_emotion'] ?? 'No emotion data',
                                style: const TextStyle(fontWeight: FontWeight.bold),
                              ),
                              subtitle: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    DateFormat('MMM dd, yyyy • HH:mm').format(createdAt),
                                    style: const TextStyle(fontSize: 12),
                                  ),
                                  if (emotionData?['mood_score'] != null)
                                    Text(
                                      'Mood: ${emotionData['mood_score']}',
                                      style: const TextStyle(fontSize: 12),
                                    ),
                                ],
                              ),
                              trailing: const Icon(Icons.chevron_right),
                              onTap: () {
                                Navigator.of(context).push(
                                  MaterialPageRoute(
                                    builder: (_) => EntryDetailScreen(entry: entry),
                                  ),
                                );
                              },
                            ),
                          );
                        },
                      ),
      ),
    );
  }

  Color _getEmotionColor(String? emotion) {
    if (emotion == null) return Colors.grey;
    
    final lowerEmotion = emotion.toLowerCase();
    if (lowerEmotion.contains('happy') || lowerEmotion.contains('joy')) {
      return Colors.green;
    } else if (lowerEmotion.contains('sad') || lowerEmotion.contains('depressed')) {
      return Colors.blue;
    } else if (lowerEmotion.contains('angry') || lowerEmotion.contains('frustrated')) {
      return Colors.red;
    } else if (lowerEmotion.contains('anxious') || lowerEmotion.contains('worried')) {
      return Colors.orange;
    } else {
      return Colors.purple;
    }
  }
}



