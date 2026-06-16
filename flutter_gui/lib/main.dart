import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';

void main() {
  runApp(const LattesCrawlerApp());
}

class LattesCrawlerApp extends StatelessWidget {
  const LattesCrawlerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Extrator Lattes',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blueGrey),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _queryController = TextEditingController();
  final TextEditingController _maxResumesController = TextEditingController(text: '0');
  
  final List<String> _logs = [];
  final ScrollController _scrollController = ScrollController();
  bool _isRunning = false;

  @override
  void dispose() {
    _queryController.dispose();
    _maxResumesController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _addLog(String message) {
    setState(() {
      _logs.add(message);
    });
    // Rola a tela para o final automaticamente
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 200),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Future<void> _runScript(String scriptName) async {
    if (_isRunning) return;

    final query = _queryController.text.trim();
    if (query.isEmpty) {
      _addLog('ERRO: Por favor, insira um termo de busca.');
      return;
    }

    setState(() {
      _isRunning = true;
      _logs.clear();
    });

    _addLog('--- Iniciando execução: $scriptName ---');
    _addLog('Termo de Busca: $query');
    _addLog('Máximo de Currículos: ${_maxResumesController.text}');
    _addLog('Aguarde...');

    try {
      // O flutter será executado dentro da pasta flutter_gui
      // Precisamos apontar para o venv e os scripts na pasta pai (selenium-lattes)
      String pythonPath = '../venv/bin/python'; 
      if (Platform.isWindows) {
        pythonPath = '..\\venv\\Scripts\\python.exe';
      }

      // IMPORTANTE: Ajuste as flags conforme o argparse dos seus scripts Python.
      // Assumindo que eles aceitem --query e --max
      List<String> args = [
        '../$scriptName',
        '--query', query,
        '--max', _maxResumesController.text
      ];

      // Inicializa o processo do Python
      final process = await Process.start(
        pythonPath, 
        args,
        workingDirectory: '..', // Executa a partir da pasta selenium-lattes
      );

      // Captura a saída padrão (stdout)
      process.stdout.transform(utf8.decoder).listen((data) {
        final lines = data.split('\n');
        for (var line in lines) {
          if (line.trim().isNotEmpty) _addLog(line.trim());
        }
      });

      // Captura erros (stderr)
      process.stderr.transform(utf8.decoder).listen((data) {
        final lines = data.split('\n');
        for (var line in lines) {
          if (line.trim().isNotEmpty) _addLog('AVISO/ERRO: ${line.trim()}');
        }
      });

      final exitCode = await process.exitCode;
      _addLog('--- Processo finalizado (Código $exitCode) ---');

    } catch (e) {
      _addLog('ERRO CRÍTICO ao iniciar o processo: $e');
    } finally {
      setState(() {
        _isRunning = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Extrator Lattes & Pipeline'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        elevation: 2,
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Área de Configuração
            Card(
              elevation: 0,
              shape: RoundedRectangleBorder(
                side: BorderSide(color: Colors.grey.shade300),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Configurações da Busca',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 16),
                    TextField(
                      controller: _queryController,
                      enabled: !_isRunning,
                      decoration: const InputDecoration(
                        labelText: 'Termo de Busca (Ex: Inteligência Artificial)',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.search),
                      ),
                    ),
                    const SizedBox(height: 16),
                    TextField(
                      controller: _maxResumesController,
                      enabled: !_isRunning,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(
                        labelText: 'Máximo de Currículos (0 para ilimitado)',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.numbers),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            
            const SizedBox(height: 24),
            
            // Botões de Ação
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                Expanded(
                  child: FilledButton.icon(
                    onPressed: _isRunning ? null : () => _runScript('main.py'),
                    icon: const Icon(Icons.download),
                    label: const Padding(
                      padding: EdgeInsets.symmetric(vertical: 16.0),
                      child: Text('Apenas Extrair', style: TextStyle(fontSize: 16)),
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: FilledButton.tonalIcon(
                    onPressed: _isRunning ? null : () => _runScript('run_pipeline.py'),
                    icon: const Icon(Icons.account_tree),
                    label: const Padding(
                      padding: EdgeInsets.symmetric(vertical: 16.0),
                      child: Text('Pipeline Completo', style: TextStyle(fontSize: 16)),
                    ),
                  ),
                ),
              ],
            ),
            
            const SizedBox(height: 24),
            
            // Console / Área de Log
            Text(
              'Console de Execução',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.grey.shade900,
                  borderRadius: BorderRadius.circular(12),
                ),
                padding: const EdgeInsets.all(16),
                child: ListView.builder(
                  controller: _scrollController,
                  itemCount: _logs.length,
                  itemBuilder: (context, index) {
                    final log = _logs[index];
                    final isError = log.startsWith('ERRO') || log.startsWith('AVISO');
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 4.0),
                      child: SelectableText(
                        log,
                        style: TextStyle(
                          color: isError ? Colors.redAccent : Colors.greenAccent,
                          fontFamily: 'monospace',
                          fontSize: 13,
                        ),
                      ),
                    );
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
