import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { theme } from './theme';   // Import the theme we just made

export default function App() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Rockbottom Insights</Text>
      
      <TouchableOpacity style={styles.uploadButton}>
        <Text style={styles.uploadText}>📸 Upload Screenshot</Text>
        <Text style={styles.subText}>or take a new one</Text>
      </TouchableOpacity>

      <Text style={styles.footer}>Analyzing your wallet • Powered by RBL</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
    alignItems: 'center',
    justifyContent: 'center',
    padding: theme.spacing.xl,
  },
  title: {
    fontSize: 28,
    color: theme.colors.primary,
    marginBottom: 40,
    fontWeight: 'bold',
    textShadowColor: theme.colors.primary,
    textShadowRadius: 10,
  },
  uploadButton: {
    backgroundColor: theme.colors.surface,
    paddingVertical: 40,
    paddingHorizontal: 60,
    borderRadius: theme.borderRadius.lg,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: theme.colors.primary,
    ...theme.shadows.glow,
  },
  uploadText: {
    color: theme.colors.primary,
    fontSize: 22,
    fontWeight: 'bold',
  },
  subText: {
    color: theme.colors.textSecondary,
    marginTop: 8,
  },
  footer: {
    marginTop: 60,
    color: theme.colors.textSecondary,
    fontSize: 14,
  },
});