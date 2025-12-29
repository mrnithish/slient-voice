import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:io';
import '../services/audio_service.dart';
import '../services/api_service.dart';
import 'entry_result_screen.dart';

class RecordingScreen extends StatefulWidget {
  const RecordingScreen({super.key});

  @override
  State<RecordingScreen> createState() => _RecordingScreenState();
}

class _RecordingScreenState extends State<RecordingScreen> {
  String? _recordedFilePath;
  bool _isUploading = false;

  @override
  Widget build(BuildContext context) {
    final audioService = Provider.of<AudioService>(context);
    final apiService = Provider.of<ApiService>(context);

    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (!audioService.isRecording && _recordedFilePath == null) ...[
                const Icon(
                  Icons.mic_none,
                  size: 120,
                  color: Colors.grey,
                ),
                const SizedBox(height: 32),
                const Text(
                  'Tap the button below to start recording',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 16, color: Colors.grey),
                ),
                const SizedBox(height: 48),
                ElevatedButton(
                  onPressed: () async {
                    final success = await audioService.startRecording();
                    if (!success && mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('Failed to start recording. Please check permissions.'),
                        ),
                      );
                    }
                  },
                  style: ElevatedButton.styleFrom(
                    shape: const CircleBorder(),
                    padding: const EdgeInsets.all(24),
                  ),
                  child: const Icon(Icons.mic, size: 48),
                ),
              ] else if (audioService.isRecording) ...[
                StreamBuilder<Duration>(
                  stream: audioService.durationStream,
                  builder: (context, snapshot) {
                    final duration = snapshot.data ?? audioService.currentDuration;
                    final minutes = duration.inMinutes;
                    final seconds = duration.inSeconds % 60;
                    
                    return Column(
                      children: [
                        Text(
                          '${minutes.toString().padLeft(2, '0')}:${seconds.toString().padLeft(2, '0')}',
                          style: const TextStyle(
                            fontSize: 48,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 16),
                        const Text(
                          'Recording...',
                          style: TextStyle(fontSize: 16, color: Colors.grey),
                        ),
                        const SizedBox(height: 48),
                        ElevatedButton(
                          onPressed: () async {
                            final path = await audioService.stopRecording();
                            if (path != null) {
                              setState(() {
                                _recordedFilePath = path;
                              });
                            }
                          },
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.red,
                            shape: const CircleBorder(),
                            padding: const EdgeInsets.all(24),
                          ),
                          child: const Icon(Icons.stop, size: 48, color: Colors.white),
                        ),
                        const SizedBox(height: 24),
                        TextButton(
                          onPressed: () async {
                            await audioService.cancelRecording();
                            setState(() {
                              _recordedFilePath = null;
                            });
                          },
                          child: const Text('Cancel'),
                        ),
                      ],
                    );
                  },
                ),
              ] else if (_recordedFilePath != null && !_isUploading) ...[
                const Icon(
                  Icons.check_circle,
                  size: 80,
                  color: Colors.green,
                ),
                const SizedBox(height: 24),
                const Text(
                  'Recording complete',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 48),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    ElevatedButton.icon(
                      onPressed: () async {
                        setState(() {
                          _isUploading = true;
                        });
                        
                        try {
                          final result = await apiService.uploadVoiceEntry(
                            File(_recordedFilePath!),
                          );
                          
                          if (mounted) {
                            Navigator.of(context).push(
                              MaterialPageRoute(
                                builder: (_) => EntryResultScreen(entry: result),
                              ),
                            );
                            setState(() {
                              _recordedFilePath = null;
                            });
                          }
                        } catch (e) {
                          if (mounted) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text('Upload failed. Please try again.'),
                              ),
                            );
                          }
                        } finally {
                          if (mounted) {
                            setState(() {
                              _isUploading = false;
                            });
                          }
                        }
                      },
                      icon: const Icon(Icons.upload),
                      label: const Text('Upload & Analyze'),
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 24,
                          vertical: 16,
                        ),
                      ),
                    ),
                    const SizedBox(width: 16),
                    TextButton(
                      onPressed: () async {
                        await audioService.cancelRecording();
                        setState(() {
                          _recordedFilePath = null;
                        });
                      },
                      child: const Text('Discard'),
                    ),
                  ],
                ),
              ] else if (_isUploading) ...[
                const CircularProgressIndicator(),
                const SizedBox(height: 24),
                const Text(
                  'Uploading and analyzing...',
                  style: TextStyle(fontSize: 16, color: Colors.grey),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}



