import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

void main() => runApp(const App());

class App extends StatefulWidget { const App({super.key}); @override State<App> createState() => _AppState(); }

class _AppState extends State<App> {
  late final WebSocketChannel ch;
  final List<Map<String, dynamic>> events = [];
  final ctrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    ch = WebSocketChannel.connect(Uri.parse('ws://localhost:8000/ws'));
    ch.stream.listen((data) {
      setState(() => events.add(jsonDecode(data)));
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: SelectionArea(
        child: Scaffold(
          appBar: AppBar(title: const Text('Nova')),
          body: Column(children: [
            Expanded(child: ListView(
              children: events.map((e) => ListTile(
                title: SelectableText(e['type'] ?? 'event'),
                subtitle: SelectableText(const JsonEncoder.withIndent('  ').convert(e)),
              )).toList(),
            )),
            Row(children: [
              Expanded(child: TextField(controller: ctrl, decoration: const InputDecoration(hintText: 'Say something'))),
              IconButton(icon: const Icon(Icons.send), onPressed: () {
                final msg = jsonEncode({"type":"user_text", "text": ctrl.text});
                ch.sink.add(msg); ctrl.clear();
              })
            ])
          ]),
        ),
      ),
    );
  }
}

