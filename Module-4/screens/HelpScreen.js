import React, { useState } from 'react';
import { StyleSheet, View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { Card } from 'react-native-elements';
import Icon from 'react-native-vector-icons/MaterialIcons';

const FAQItem = ({ question, answer }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <Card containerStyle={styles.faqCard}>
      <TouchableOpacity
        style={styles.faqHeader}
        onPress={() => setIsExpanded(!isExpanded)}
      >
        <Text style={styles.question}>{question}</Text>
        <Icon
          name={isExpanded ? 'keyboard-arrow-up' : 'keyboard-arrow-down'}
          size={24}
          color="#666"
        />
      </TouchableOpacity>
      {isExpanded && <Text style={styles.answer}>{answer}</Text>}
    </Card>
  );
};

const HelpScreen = () => {
  const faqs = [
    {
      id: '1',
      question: 'How do I use the building recognition feature?',
      answer: 'Simply tap the camera button and take a photo of the building. The app will automatically recognize the building and show you its location on the map.',
    },
    {
      id: '2',
      question: 'How accurate is the distance estimation?',
      answer: 'The distance estimation is typically accurate within 5-10 meters, depending on lighting conditions and image quality.',
    },
    {
      id: '3',
      question: 'Can I save my favorite buildings?',
      answer: 'Yes, you can mark buildings as favorites by tapping the heart icon in the building directory or details screen.',
    },
    {
      id: '4',
      question: 'How do I get directions to a building?',
      answer: 'In the building details screen, tap the "Get Directions" button to open your preferred navigation app with the building location.',
    },
    {
      id: '5',
      question: 'Is my location data stored?',
      answer: 'Your location history is stored locally on your device and can be cleared in the Settings screen.',
    },
  ];

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Help & Support</Text>
        <Text style={styles.subtitle}>Find answers to common questions</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Frequently Asked Questions</Text>
        {faqs.map(faq => (
          <FAQItem
            key={faq.id}
            question={faq.question}
            answer={faq.answer}
          />
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Contact Support</Text>
        <Card containerStyle={styles.contactCard}>
          <Text style={styles.contactText}>
            If you need further assistance, please contact our support team:
          </Text>
          <Text style={styles.contactInfo}>📧 support@campusnav.com</Text>
          <Text style={styles.contactInfo}>📞 +1 (555) 123-4567</Text>
          <Text style={styles.contactInfo}>🕒 Mon-Fri: 9:00 AM - 5:00 PM</Text>
        </Card>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>App Information</Text>
        <Card containerStyle={styles.infoCard}>
          <Text style={styles.infoText}>Version: 1.0.0</Text>
          <Text style={styles.infoText}>Last Updated: March 15, 2024</Text>
          <Text style={styles.infoText}>© 2024 Campus Navigation Assistant</Text>
        </Card>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 20,
    backgroundColor: '#007AFF',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#fff',
    opacity: 0.8,
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  faqCard: {
    borderRadius: 10,
    marginBottom: 10,
    padding: 15,
  },
  faqHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  question: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
  },
  answer: {
    fontSize: 14,
    color: '#666',
    marginTop: 10,
    lineHeight: 20,
  },
  contactCard: {
    borderRadius: 10,
    padding: 15,
  },
  contactText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 15,
  },
  contactInfo: {
    fontSize: 16,
    color: '#333',
    marginBottom: 10,
  },
  infoCard: {
    borderRadius: 10,
    padding: 15,
  },
  infoText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
  },
});

export default HelpScreen; 