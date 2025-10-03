from django.db import models


class UnreadMessagesManager(models.Manager):
    """Manager to return unread messages for a given user, optimized for inbox listing."""
    def unread_for_user(self, user):
        # Use select_related to bring sender in a single query and only select required fields
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .select_related('sender', 'parent_message')
            .prefetch_related('replies')
            .only(
                'message_id', 
                'sender__username', 
                'content', 
                'sent_at',
                'parent_message__message_id',
                'read'
            )
            .order_by('-sent_at')
        )
    
    def mark_as_read(self, message_ids, user):
        """Mark multiple messages as read for a user."""
        return (
            self.get_queryset()
            .filter(
                message_id__in=message_ids,
                receiver=user,
                read=False
            )
            .update(read=True)
        )
    
    def unread_count_for_user(self, user):
        """Get the count of unread messages for a user."""
        return self.get_queryset().filter(
            receiver=user,
            read=False
        ).count()

    # Backwards-compatible alias used in older tests/code
    def unread_for(self, user):
        return self.unread_for_user(user)

    def thread_for_message(self, message_id):
        """Return a nested dict representing the message thread rooted at message_id.

        This fetches the root message and then iteratively fetches child levels using
        the manager's queryset to avoid putting filters in views. Uses select_related
        to load senders and only() to limit selected fields.
        """
        qs = (
            self.get_queryset()
            .select_related('sender')
            .only('message_id', 'content', 'sent_at', 'sender__username', 'parent_message')
            # Prefetch up to three levels of replies (covers common threading depths)
            .prefetch_related('replies__sender', 'replies__replies__sender', 'replies__replies__replies__sender')
        )

        # Get root message with replies prefetched
        root = qs.get(message_id=message_id)

        # Traverse prefetched relations to collect nodes without extra DB hits
        all_nodes = {root.message_id: root}

        def walk(node):
            # node.replies.all() is prefetched for up to the configured depth
            for child in getattr(node, 'replies').all():
                all_nodes[child.message_id] = child
                walk(child)

        walk(root)

        # Build parent->children map using parent_message_id from prefetched objects
        children_map = {}
        for node in all_nodes.values():
            pid = getattr(node.parent_message, 'message_id', None)
            children_map.setdefault(pid, []).append(node)

        def build_node(msg):
            node = {
                'message_id': str(msg.message_id),
                'sender': getattr(msg.sender, 'username', None),
                'content': msg.content,
                'sent_at': msg.sent_at.isoformat(),
                'replies': [],
            }
            for child in children_map.get(msg.message_id, []):
                if child.message_id == msg.message_id:
                    # skip self references just in case
                    continue
                node['replies'].append(build_node(child))
            return node

        return build_node(root)

    def thread_for_message_recursive(self, message_id):
        """Build thread using iterative ORM filters (recursive via repeated queries).

        This method demonstrates a recursive fetch using Django ORM: it finds the
        root message and then repeatedly queries for children whose parent is in
        the current set until no more descendants are found.
        """
        qs = (
            self.get_queryset()
            .select_related('sender')
            .only('message_id', 'content', 'sent_at', 'sender__username', 'parent_message')
        )

        root = qs.get(message_id=message_id)

        all_nodes = {root.message_id: root}
        # start with root pk list
        current_ids = [root.pk]
        while current_ids:
            children_qs = qs.filter(parent_message__pk__in=current_ids)
            children = list(children_qs)
            if not children:
                break
            for c in children:
                all_nodes[c.message_id] = c
            current_ids = [c.pk for c in children]

        # Build parent->children map
        children_map = {}
        for node in all_nodes.values():
            pid = getattr(node.parent_message, 'message_id', None)
            children_map.setdefault(pid, []).append(node)

        def build_node(msg):
            node = {
                'message_id': str(msg.message_id),
                'sender': getattr(msg.sender, 'username', None),
                'content': msg.content,
                'sent_at': msg.sent_at.isoformat(),
                'replies': [],
            }
            for child in children_map.get(msg.message_id, []):
                if child.message_id == msg.message_id:
                    continue
                node['replies'].append(build_node(child))
            return node

        return build_node(root)
