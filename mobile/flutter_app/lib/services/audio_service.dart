import 'dart:async';
import 'package:record/record.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:io';

class AudioService {
  final AudioRecorder _recorder = AudioRecorder();
  bool _isRecording = false;
  String? _currentRecordingPath;
  Timer? _durationTimer;
  Duration _recordingDuration = Duration.zero;
  final StreamController<Duration> _durationController = StreamController<Duration>.broadcast();
  
  bool get isRecording => _isRecording;
  String? get currentRecordingPath => _currentRecordingPath;
  Stream<Duration> get durationStream => _durationController.stream;
  Duration get currentDuration => _recordingDuration;
  
  Future<bool> requestPermissions() async {
    final status = await Permission.microphone.request();
    return status.isGranted;
  }
  
  Future<bool> startRecording() async {
    try {
      if (_isRecording) {
        return false;
      }
      
      // Check permissions
      if (!await requestPermissions()) {
        return false;
      }
      
      // Get temporary directory
      final directory = await getTemporaryDirectory();
      final timestamp = DateTime.now().millisecondsSinceEpoch;
      _currentRecordingPath = '${directory.path}/recording_$timestamp.m4a';
      
      // Start recording
      await _recorder.start(
        const RecordConfig(
          encoder: AudioEncoder.aacLc,
          bitRate: 128000,
          sampleRate: 44100,
        ),
        path: _currentRecordingPath!,
      );
      
      _isRecording = true;
      _recordingDuration = Duration.zero;
      
      // Start duration timer
      _durationTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
        _recordingDuration = _recordingDuration + const Duration(seconds: 1);
        _durationController.add(_recordingDuration);
        
        // Stop at 5 minutes max
        if (_recordingDuration.inMinutes >= 5) {
          stopRecording();
        }
      });
      
      return true;
    } catch (e) {
      print('Error starting recording: $e');
      return false;
    }
  }
  
  Future<String?> stopRecording() async {
    try {
      if (!_isRecording) {
        return null;
      }
      
      final path = await _recorder.stop();
      _isRecording = false;
      _durationTimer?.cancel();
      _durationTimer = null;
      
      return path;
    } catch (e) {
      print('Error stopping recording: $e');
      _isRecording = false;
      _durationTimer?.cancel();
      _durationTimer = null;
      return null;
    }
  }
  
  Future<void> cancelRecording() async {
    try {
      if (_isRecording) {
        await _recorder.stop();
        _isRecording = false;
        _durationTimer?.cancel();
        _durationTimer = null;
      }
      
      // Delete the file if it exists
      if (_currentRecordingPath != null) {
        final file = File(_currentRecordingPath!);
        if (await file.exists()) {
          await file.delete();
        }
        _currentRecordingPath = null;
      }
      
      _recordingDuration = Duration.zero;
      _durationController.add(_recordingDuration);
    } catch (e) {
      print('Error cancelling recording: $e');
    }
  }
  
  void dispose() {
    _durationTimer?.cancel();
    _durationController.close();
    _recorder.dispose();
  }
}



