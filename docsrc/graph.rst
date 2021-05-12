========================
Model Visualization
========================

Here is an overview of the project's data model. For the initial implementation this is set up to be utilized for only a single application review cycle. Future enhancements will include the ability to have multiple application cycles and to be able to analyze performance across cycles.

For applications like this where you are going to have multiple people working on them, it is useful to have :code:`created_date` and :code:`last_modified` (as well as :code:`last_modified_by`, not yet implemented) fields on all objects to be able to see when things changed and who changed them. :class:`grants.models.TimeStampMixin` (at the bottom of the graph) accomplishe by having the other models inherit from this one. To avoid inadvertently creating instances of :code:`TimeStampMixin`, the :code:`Meta.abstract` property is set to :code:`True`.

The documentation on the :doc:`Models <models>` includes implementation details, but at a high level, the task at hand to to collect scores from reviewers to a common set of questions for each application. Formally, there are :class:`grants.models.ReviewQuestion` (s), that represent a common question to be ansswered by multiple :class:`grants.models.Reviewer` (s) for each :class:`grants.models.Application` . This is accomplished through the use of a :class:`grants.models.ReviewAnswer` and a :class:`grants.models.Assignment` . The assignment is a relationship between an application and a reviewer and the api will be set up to create a :class:`grants.models.ReviewAnswer` for each question that contain the reviewers response to the questions. This gets related back to the application through the assignment.

.. graphviz:: _static/grants_models.dot

