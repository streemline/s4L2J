import sys
from com.l2jserver.gameserver.model.quest		import State
from com.l2jserver.gameserver.model.quest		import QuestState
from com.l2jserver.gameserver.model.quest.jython	import QuestJython as JQuest

from com.l2jserver.gameserver.datatables import SkillTable #�ޯत��W����
from com.l2jserver.gameserver.datatables import SkillTreesData #�ǲߧޯ����
from com.l2jserver.gameserver.model import L2SkillLearn #�ǲߧޯ����
from com.l2jserver.gameserver.model.skills import L2Skill #�ޯ����



class EasySkillLearn(JQuest):
	qID = -1
	qn = "easySkillLearn"
	qDesc = "custom"
	
	NPCID = [103] #Ĳ�o���Ȫ� NPC �i�ק�.. �i�H�h ID �Ҧp [100,102,103]
	
	includeByFs = True #�O�_�]�A��ѯ��ǧޯ�
	includeAutoGet = True
	
	htm_header = "<html><body><title>²���ޯ�ǲߨt��</title>"
	htm_footer = "</body></html>"
	
	def __init__(self, id = qID, name = qn, descr = qDesc):
		JQuest.__init__(self, id, name, descr)
		for id in self.NPCID:
			self.addStartNpc(id)
			self.addFirstTalkId(id)
			self.addTalkId(id)
		print "Init:" + self.qn + " loaded"

	def getAvailableSkill(self, player):
		return SkillTreesData.getInstance().getAvailableSkills(player, player.getClassId(), self.includeByFs, self.includeAutoGet)
		
	def listAvailableSkill(self, player):
		sl = self.getAvailableSkill(player)
		r = "�i�ǲߪ��ޯ�M��<br1>"
		r += '<a action="bypass -h Quest %s learn_all">�����ǲ�</a><br1>' % self.qn
		skillTable = SkillTable.getInstance()
		for s in sl:
			r += "<a action=\"bypass -h Quest " + self.qn + " learn " + str(s.getSkillId()) + " " + str(s.getSkillLevel()) + "\">" + skillTable.getInfo(s.getSkillId(), s.getSkillLevel()).getName() + " Lv " + str(s.getSkillLevel()) + "</a><BR1>"
		return r

	def myAddSkill(self, player, id):
		sl = self.getAvailableSkill(player)
		for s in sl:
			if s.getSkillId() == id:
				player.addSkill(SkillTable.getInstance().getInfo(s.getSkillId(), s.getSkillLevel()), True)
				self.myAddSkill(player, id)
				break

	def onAdvEvent(self, event, npc, player):
		if event == 'learn_all':
			sl = self.getAvailableSkill(player)
			c = 0
			while sl:
				player.addSkill(SkillTable.getInstance().getInfo(sl[0].getSkillId(), sl[0].getSkillLevel()), True)
				sl = self.getAvailableSkill(player)
				c += 1
				if c > 5000:
					return self.htm_header + "��������ޯ�ǧ� �ЦA�դ@�� �λP GM �p��" + self.htm_footer #�ޯ��ƥX�{���D �Ц^��
			player.sendSkillList()
			return self.htm_header + "�����ޯ�ǧ� %s" % ["(���]�A��ѯ��ǧޯ�)","(�]�A��ѯ��ǧޯ�)"][self.includeByFs] + self.htm_footer
		if event.startswith('learn '):
			sid, slv = event[6:].split()
			sid = int(sid)
			slv = int(slv)
			self.myAddSkill(player, sid)
			player.sendSkillList()
		return self.onFirstTalk(npc, player)
		
	def onFirstTalk(self, npc, player):
		st = player.getQuestState(self.qn)
		if not st:
			st = self.newQuestState(player)
			st.setState(State.STARTED)
		return self.htm_header + self.listAvailableSkill(player) + self.htm_footer
		
EasySkillLearn()