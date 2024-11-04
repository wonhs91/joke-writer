"use client";

import React from 'react';

import { Button } from '@/components/ui/button';

interface KyewordAssociationsCardProps {
  keyword: string
  associations: string[];
  selectedAssociation: string;
  isLoading: boolean;
  onAssociationSelect: (keyword: string, association: string) => void;
}

const KeywordAssociationsCard: React.FC<KyewordAssociationsCardProps> = ({
  keyword,
  associations,
  selectedAssociation,
  isLoading,
  onAssociationSelect
}) => {

  return (
    <div>
    <div className="flex justify-between items-center">{keyword}</div>
    <div className="flex flex-wrap gap-2">
    {associations.map((association: string) => (
      <Button
        key={association}
        variant={selectedAssociation == association ? "default" : "outline"}
        onClick={() => onAssociationSelect(keyword, association)}
        disabled={isLoading}
      >
        {association}
      </Button>
    ))}
  </div>
  </div>
  )
}

export default KeywordAssociationsCard;