// Tessitura\frontend\App.tsx
import React, { useState } from 'react';
import { StyleSheet, Text, View, Button } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import axios from 'axios';

export default function App() {
  const [tabs, setTabs] = useState('');

  const fetchTabs = async () => {
    try {
      const response = await axios.post('http://10.0.2.2:5000/convert');
      //const response = await axios.post('http://localhost:5000/convert');
      setTabs(response.data.tabs.join('\n')); 
    } catch (error) {
      console.error('Failed to fetch tabs:', error);
      setTabs('Failed to load tabs');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Espresso Trial</Text>
      <Button title="Get Tabs" onPress={fetchTabs} />
      <Text style={styles.tabs}>{tabs}</Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  tabs: {
    fontFamily: 'monospace',
    fontSize: 16,
    marginTop: 20,
    textAlign: 'left',
    alignSelf: 'stretch',
  },
});
