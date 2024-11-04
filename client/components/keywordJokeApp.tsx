"use client";

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import KeywordInput from './keywordInput';
import KeywordAssociationsCard from './KeywordAssociationsCard';
import { Button } from '@/components/ui/button';

interface KeywordAssociations {
  [key: string]: string[];
}

interface AssociatedWordsResponse {
  thread_id: string;
  keys_associations: { [key: string]: string[] };
}

interface KyesAssociations {
  keys_associations: { [keyword: string]: string[]}
}

interface JokeMaterials {
  materials: { [keyword: string]: string}
}

interface JokeResponse {
  keywords?: string[];
  keywords_associations?: KyesAssociations
  joke_material: JokeMaterials
  joke: string;
}

// Keyword Input Component


const KeywordJokeApp: React.FC = () => {
  const [keywords, setKeywords] = useState<string[]>([]);
  const [keywordsAssociations, setKeywordsAssociations] = useState<KeywordAssociations>({});
  const [selectedAssociations, setSelectedAssociations] = useState<{ [key: string]: string}>({})

  const [joke, setJoke] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [threadId, setThreadId] = useState<string>('');

  const handleAddKeyword = (keyword: string): void => {
    setKeywords([...keywords, keyword]);
  };

  const handleRemoveKeyword = (keywordToRemove: string): void => {
    setKeywords(keywords.filter(k => k !== keywordToRemove));
  };

  const handleKeywordSubmit = async (): Promise<void> => {
    if (keywords.length === 0) return;

    setLoading(true);
    try {
      const request = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ keywords })
      }
      const response = await fetch('http://localhost:8000/api/joke-writer/associations', request);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: AssociatedWordsResponse = await response.json();
      setKeywordsAssociations(data.keys_associations);
      setThreadId(data.thread_id);
      setJoke('');
      setSelectedAssociations({});
    } catch (error) {
      console.error('Error fetching associated words:', error);
      setKeywordsAssociations({});
    } finally {
      setLoading(false);
    }
  };

  const handleWordSelect = async (keyword: string, association: string): Promise<void> => {
    setSelectedAssociations({
      ...selectedAssociations,
      [keyword]: association
    });
  };

  const handleAssociationsSubmit = async (): Promise<void> => {
    setLoading(true);
    try {
      const request = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(selectedAssociations)
      }
      const response = await fetch(`http://localhost:8000/api/joke-writer/joke/${threadId}`, request);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: JokeResponse = await response.json();
      setJoke(data.joke);
    } catch (error) {
      console.error('Error generating joke:', error);
      setJoke('');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4 space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>Keyword to Joke Generator</CardTitle>
          <CardDescription>
            Enter multiple keywords to find associated words and generate jokes
          </CardDescription>
        </CardHeader>
        <CardContent>
          <KeywordInput
            keywords={keywords}
            onAddKeyword={handleAddKeyword}
            onRemoveKeyword={handleRemoveKeyword}
            onSubmit={handleKeywordSubmit}
            isLoading={loading}
          />
        </CardContent>
      </Card>

      {Object.keys(keywordsAssociations).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Associated Words</CardTitle>
          </CardHeader>
          <CardContent>
            {Object.entries(keywordsAssociations).map(([keyword, associations]) => (
              <KeywordAssociationsCard
                key={keyword}
                keyword={keyword}
                associations={associations}
                selectedAssociation={selectedAssociations?.[keyword] !== undefined ? selectedAssociations[keyword] : ""}
                onAssociationSelect={handleWordSelect}
                isLoading={loading}
              />
            ))}
            <Button
              className="mt-4"
              onClick={handleAssociationsSubmit}
              disabled={loading}
            />
          </CardContent>
        </Card>
      )}

      {joke && (
        <Card>
          <CardHeader>
            <CardTitle>Generated Joke</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-lg">{joke}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default KeywordJokeApp;