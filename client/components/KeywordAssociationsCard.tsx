import React from 'react';

import { Button } from '@/components/ui/button';

interface KyewordAssociationsCardProps {
  keyword: string
  associations: string[];
  selectedAssociations: string[];
  isLoading: boolean;
  onAssociationSelect: (keyword: string, association: string) => void;
}

const KeywordAssociationsCard: React.FC<KyewordAssociationsCardProps> = ({
  keyword,
  associations,
  selectedAssociations,
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
        variant={selectedAssociations.includes(association) ? "default" : "outline"}
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