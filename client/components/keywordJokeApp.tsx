"use client";

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import KeywordInput from './keywordInput';
import KeywordAssociationsCard from './KeywordAssociationsCard';
import { Button } from '@/components/ui/button';



interface Associations {
  keyword: string;
  associations: string[];
}

interface KeywordAssociations {
  [key: string]: string[];
}

interface AssociatedWordsResponse {
  thread_id: string;
  agent_response: { keywords: string[], keywords_associations: Associations[] };
}

interface JokeResponse {
  joke: string;
}

// Keyword Input Component


const KeywordJokeApp: React.FC = () => {
  const [keywords, setKeywords] = useState<string[]>([]);
  const [keywordsAssociations, setKeywordsAssociations] = useState<Associations[]>([]);
  const [selectedWord, setSelectedWord] = useState<string>('');
  const [selectedKeywordsAssociations, setSelectedKeywordsAssociations] = useState<KeywordAssociations>({})

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
      const response = await fetch('http://localhost:8000/api/joke-writer/associations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ keywords })
      });
      console.log(`this is public api url: ${process.env.NEXT_PUBLIC_API_URL}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: AssociatedWordsResponse = await response.json();
      setKeywordsAssociations(data.agent_response.keywords_associations);
      setThreadId(data.thread_id);
      setJoke('');
      setSelectedWord('');
      setSelectedKeywordsAssociations({});
    } catch (error) {
      console.error('Error fetching associated words:', error);
      setKeywordsAssociations([]);
    } finally {
      setLoading(false);
    }
  };

  const handleWordSelect = async (keyword: string, association: string): Promise<void> => {
    setSelectedKeywordsAssociations({
      ...selectedKeywordsAssociations,
      keyword: [...selectedKeywordsAssociations[keyword], association]
    });
  };

  const handleAssociationsSubmit = async (): Promise<void> => {
    setLoading(true);
    try {
      const response = await fetch(`/joke-writer/joke/${threadId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ selectedKeywordsAssociations })
      });

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

      {keywordsAssociations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Associated Words</CardTitle>
          </CardHeader>
          <CardContent>
            {keywordsAssociations.map(keywordAssociation => (
              <KeywordAssociationsCard
                key={keywordAssociation.keyword}
                keyword={keywordAssociation.keyword}
                associations={keywordAssociation.associations}
                selectedAssociations={selectedKeywordsAssociations[keywordAssociation.keyword]}
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