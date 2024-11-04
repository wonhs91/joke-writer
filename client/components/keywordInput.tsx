"use client";

import React, { useState } from 'react';
import { Search, Loader2, AlertCircle, X } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';


// Types and Interfaces
interface KeywordInputProps {
  keywords: string[];
  onAddKeyword: (keyword: string) => void;
  onRemoveKeyword: (keyword: string) => void;
  onSubmit: () => void;
  isLoading: boolean;
}


const KeywordInput: React.FC<KeywordInputProps> = ({
  keywords,
  onAddKeyword,
  onRemoveKeyword,
  onSubmit,
  isLoading
}) => {
  const [inputValue, setInputValue] = useState<string>('');
  const [error, setError] = useState<string>('');

  const validateKeyword = (input: string): boolean => {
    const trimmedInput = input.trim();
    
    // Check if keyword already exists
    if (keywords.includes(trimmedInput.toLowerCase())) {
      setError('This keyword has already been added');
      return false;
    }
    
    // Check if input contains special characters
    if (!/^[a-zA-Z0-9]+$/.test(trimmedInput)) {
      setError('Please use only letters and numbers');
      return false;
    }
    
    // Clear error if validation passes
    setError('');
    return true;
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
    const input = e.target.value;
    setInputValue(input);
    if (input) {
      validateKeyword(input);
    } else {
      setError('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>): void => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddKeyword();
    }
  };

  const handleAddKeyword = (): void => {
    const trimmedInput = inputValue.trim();
    if (trimmedInput && validateKeyword(trimmedInput)) {
      onAddKeyword(trimmedInput.toLowerCase());
      setInputValue('');
      setError('');
    }
  };

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <div className="flex gap-2">
          <Input
            id="keyword-input"
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Type a keyword and press Enter..."
            className="flex-1"
            aria-invalid={!!error}
          />
          <Button 
            type="button" 
            onClick={handleAddKeyword}
            disabled={!inputValue.trim() || !!error}
          >
            Add
          </Button>
        </div>
        {error && (
          <Alert variant="destructive" className="mt-2">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
      </div>

      <div className="flex flex-wrap gap-2">
        {keywords.map((keyword) => (
          <div
            key={keyword}
            className="flex items-center gap-1 bg-primary text-primary-foreground px-3 py-1 rounded-full text-sm"
          >
            {keyword}
            <button
              onClick={() => onRemoveKeyword(keyword)}
              className="hover:text-red-300 transition-colors"
              type="button"
              aria-label={`Remove ${keyword}`}
            >
              <X className="h-3 w-3" />
            </button>
          </div>
        ))}
      </div>

      {keywords.length > 0 && (
        <Button 
          onClick={onSubmit}
          disabled={isLoading || keywords.length < 2}
          className="w-full"
        >
          {isLoading ? (
            <Loader2 className="h-4 w-4 animate-spin mr-2" />
          ) : (
            <Search className="h-4 w-4 mr-2" />
          )}
          Find Associated Words
        </Button>
      )}
    </div>
  );
};

export default KeywordInput;