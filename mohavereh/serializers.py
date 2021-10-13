from rest_framework import serializers
from mohavereh.models import InformalText,FormalText

class FormalTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormalText
        fields = ['answer_body','informalـtext']

class InformalTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformalText
        #phase2.5 validate_answer is new and blocked_by_person_for_answering,id,blocked_by_person_for_validating phase2.6 ,#add still_blocked,start_time phase3.4
        fields = ['text','slug','has_answer','validate_answer','blocked_by_person_for_answering','id','blocked_by_person_for_validating','start_time','still_blocked'] 
        
class InformalAndAnswerSerializer(serializers.Serializer):
    informal = InformalTextSerializer()
    formal = FormalTextSerializer(many=True)      