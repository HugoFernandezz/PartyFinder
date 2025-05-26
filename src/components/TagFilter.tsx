import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export interface TagFilterProps {
  availableTags: string[];
  selectedTags: string[];
  onTagToggle: (tag: string) => void;
}

export const TagFilter: React.FC<TagFilterProps> = ({
  availableTags,
  selectedTags,
  onTagToggle,
}) => {
  const getTagIcon = (tag: string): keyof typeof Ionicons.glyphMap => {
    switch (tag.toLowerCase()) {
      case 'fiestas':
      case 'fiesta':
        return 'musical-notes';
      case 'buses':
        return 'bus';
      case 'otros eventos':
        return 'calendar';
      default:
        return 'pricetag';
    }
  };

  const getTagColor = (tag: string, isSelected: boolean) => {
    if (isSelected) {
      switch (tag.toLowerCase()) {
        case 'fiestas':
        case 'fiesta':
          return { bg: '#FF6B6B', text: '#fff' };
        case 'buses':
          return { bg: '#FD79A8', text: '#fff' };
        case 'otros eventos':
          return { bg: '#4ECDC4', text: '#fff' };
        default:
          return { bg: '#6366f1', text: '#fff' };
      }
    } else {
      return { bg: '#f3f4f6', text: '#6b7280' };
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Filtrar por categorias</Text>
      <ScrollView 
        horizontal 
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {availableTags.map((tag) => {
          const isSelected = selectedTags.includes(tag);
          const colors = getTagColor(tag, isSelected);
          const icon = getTagIcon(tag);

          return (
            <TouchableOpacity
              key={tag}
              style={[
                styles.tagButton,
                { backgroundColor: colors.bg }
              ]}
              onPress={() => onTagToggle(tag)}
              activeOpacity={0.7}
            >
              <Ionicons 
                name={icon} 
                size={16} 
                color={colors.text} 
                style={styles.tagIcon}
              />
              <Text style={[styles.tagText, { color: colors.text }]}>
                {tag}
              </Text>
              {isSelected && (
                <Ionicons 
                  name="checkmark-circle" 
                  size={16} 
                  color={colors.text}
                  style={styles.checkIcon}
                />
              )}
            </TouchableOpacity>
          );
        })}
      </ScrollView>
      
      {selectedTags.length > 0 && (
        <View style={styles.selectedInfo}>
          <Text style={styles.selectedText}>
            {selectedTags.length} categoria{selectedTags.length !== 1 ? 's' : ''} seleccionada{selectedTags.length !== 1 ? 's' : ''}
          </Text>
          <TouchableOpacity
            onPress={() => selectedTags.forEach(tag => onTagToggle(tag))}
            style={styles.clearButton}
          >
            <Text style={styles.clearText}>Limpiar todo</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 12,
    paddingHorizontal: 20,
  },
  scrollContent: {
    paddingHorizontal: 20,
    gap: 8,
  },
  tagButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
    marginRight: 8,
    minHeight: 36,
  },
  tagIcon: {
    marginRight: 6,
  },
  tagText: {
    fontSize: 14,
    fontWeight: '500',
  },
  checkIcon: {
    marginLeft: 4,
  },
  selectedInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 12,
  },
  selectedText: {
    fontSize: 14,
    color: '#6b7280',
  },
  clearButton: {
    paddingHorizontal: 12,
    paddingVertical: 4,
  },
  clearText: {
    fontSize: 14,
    color: '#6366f1',
    fontWeight: '500',
  },
}); 