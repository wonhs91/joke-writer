"use client";

import React, { useState } from 'react';
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input'
import { Plus } from 'lucide-react'


interface KyewordAssociationsCardProps {
  keyword: string
  associations: string[];
  selectedAssociation: string;
  isLoading: boolean;
  onAssociationSelect: (keyword: string, association: string) => void;
  onAddCustomAssociation: (keyword: string, association: string) => void;
}

const KeywordAssociationsCard: React.FC<KyewordAssociationsCardProps> = ({
  keyword,
  associations,
  selectedAssociation,
  isLoading,
  onAssociationSelect,
  onAddCustomAssociation
}) => {

  const [customAssociation, setCustomAssociation] = useState('')
  const handleAddCustomAssociation = () => {
    if (customAssociation.trim()) {
      onAddCustomAssociation(keyword, customAssociation.trim())
      setCustomAssociation('')
    }
  }

  return (
    <div className="space-y-2">
      <Label className="text-lg font-semibold" htmlFor="keyword">{keyword}</Label>
      <div className="flex flex-wrap gap-2 ">
        {associations.map((association: string) => (
          <Button 
            className="flex-shrink-0"
            key={association}
            variant={selectedAssociation == association ? "default" : "outline"}
            onClick={() => onAssociationSelect(keyword, association)}
            disabled={isLoading}
          >
            {association}
          </Button>
        ))}
      </div>  
      <div className="flex gap-2">
        <Input
          id={`custom-association-${keyword}`}
          value={customAssociation}
          onChange={(e) => setCustomAssociation(e.target.value)}
          placeholder="Add custom association"
          disabled={isLoading}
          className="flex-grow"
        />
        <Button
          onClick={handleAddCustomAssociation}
          disabled={isLoading || !customAssociation.trim()}
          variant="outline"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add
        </Button>
      </div>
    </div>
  )
}

export default KeywordAssociationsCard;